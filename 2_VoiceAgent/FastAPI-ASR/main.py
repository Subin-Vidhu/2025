import uvicorn
from fastapi import FastAPI, WebSocket, UploadFile, File, Form, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import requests
import tempfile
import os
import asyncio
import logging
from pathlib import Path
import uuid
import time
import io
import subprocess

# Import our audio utilities
from audio_utils import ensure_required_format, get_audio_info, FFMPEG_AVAILABLE

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Real-time ASR with FastAPI")

# Add CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# ASR API URL
ASR_API_URL = "https://canary.protosonline.in"

# Maximum retries for API calls
MAX_API_RETRIES = 2

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.temp_audio_files = {}
        self.temp_chunk_files = {}  # Store individual chunk files
        self.last_processed_time = {}
        self.audio_data = {}  # Store complete audio data for each client
        self.last_transcription = {}  # Store the last transcription for each client
        self.chunk_counter = {}  # Count chunks for each client

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.temp_audio_files[client_id] = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        self.temp_chunk_files[client_id] = []  # Initialize empty list for chunk files
        self.last_processed_time[client_id] = time.time()
        self.audio_data[client_id] = bytearray()  # Initialize empty bytearray for audio data
        self.last_transcription[client_id] = ""  # Initialize last transcription to empty string
        self.chunk_counter[client_id] = 0  # Initialize chunk counter
        logger.info(f"Client {client_id} connected. Temp file: {self.temp_audio_files[client_id].name}")
        return self.temp_audio_files[client_id]

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        # Close and remove temporary file
        if client_id in self.temp_audio_files:
            temp_file = self.temp_audio_files[client_id]
            temp_file.close()
            try:
                os.unlink(temp_file.name)
                logger.info(f"Removed temp file: {temp_file.name}")
            except Exception as e:
                logger.error(f"Error removing temp file: {e}")
            del self.temp_audio_files[client_id]
        
        # Clean up any chunk files
        if client_id in self.temp_chunk_files:
            for chunk_file in self.temp_chunk_files[client_id]:
                try:
                    os.unlink(chunk_file)
                    logger.debug(f"Removed chunk file: {chunk_file}")
                except Exception as e:
                    logger.error(f"Error removing chunk file: {e}")
            del self.temp_chunk_files[client_id]
            
        if client_id in self.last_processed_time:
            del self.last_processed_time[client_id]
        
        if client_id in self.audio_data:
            del self.audio_data[client_id]
            
        if client_id in self.last_transcription:
            del self.last_transcription[client_id]
            
        if client_id in self.chunk_counter:
            del self.chunk_counter[client_id]
            
        logger.info(f"Client {client_id} disconnected")

    async def send_transcription(self, client_id: str, message: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)


manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_root():
    # Return the index.html file from the static directory
    index_path = static_dir / "index.html"
    if not index_path.exists():
        return HTMLResponse(content="<html><body><h1>Error: index.html not found</h1><p>The static/index.html file was not found.</p></body></html>")
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except UnicodeDecodeError:
        # Fallback to a simpler encoding or provide a basic page
        logger.error(f"Error reading index.html: Unicode decode error")
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Speech Recognition</title>
            <style>
                body { font-family: Arial, sans-serif; text-align: center; margin: 50px; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <h1>Speech Recognition</h1>
            <p class="error">There was an error loading the main interface.</p>
            <p>Please try refreshing the page or contact support.</p>
        </body>
        </html>
        """)

@app.get("/api/status")
async def get_api_status():
    """API status endpoint that returns JSON"""
    # Check if the ASR API is accessible
    api_status = "unknown"
    try:
        # Make a simple HEAD request to check if the server is up
        response = requests.head(ASR_API_URL, timeout=3)
        api_status = "up" if response.status_code < 400 else "down"
    except requests.RequestException:
        api_status = "down"
        
    return {
        "message": "Real-time ASR API is running. Connect to /ws for real-time transcription.",
        "ffmpeg_available": FFMPEG_AVAILABLE,
        "asr_api_status": api_status
    }

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    temp_file = await manager.connect(websocket, client_id)
    
    try:
        # Track accumulated audio data
        accumulated_size = 0
        last_transcription_attempt = time.time()
        transcription_interval = 1.5  # seconds - shorter interval for more responsive real-time transcription
        min_audio_duration = 0.5  # Minimum audio duration in seconds - shorter for quicker feedback
        
        while True:
            # Receive binary audio data from client
            data = await websocket.receive_bytes()
            
            # Store the audio data in the temporary file
            temp_file.write(data)
            temp_file.flush()
            accumulated_size += len(data)
            
            # Only attempt transcription at intervals to avoid overwhelming the server
            current_time = time.time()
            elapsed_since_last_transcription = current_time - last_transcription_attempt
            
            # Process audio periodically 
            if elapsed_since_last_transcription > transcription_interval:
                # Get the current size of the accumulated audio
                file_size = temp_file.tell()
                
                # Estimate duration (assuming 16-bit mono PCM at 16kHz)
                # Each sample is 2 bytes, so duration = size / (sample_rate * bytes_per_sample)
                estimated_duration = file_size / (16000 * 2)
                
                logger.info(f"Processing audio for client {client_id} - Size: {file_size} bytes, Est. duration: {estimated_duration:.2f}s")
                
                # Only process if we have enough audio data
                if estimated_duration >= min_audio_duration:
                    try:
                        # Make a copy of the temp file to avoid conflicts during processing
                        temp_processing_path = os.path.join(
                            tempfile.gettempdir(),
                            f"processing_{client_id}_{int(current_time)}.wav"
                        )
                        
                        # Add to list of temp files to clean up later
                        manager.temp_chunk_files[client_id].append(temp_processing_path)
                        
                        # Copy the file for processing
                        with open(temp_file.name, 'rb') as src, open(temp_processing_path, 'wb') as dst:
                            dst.write(src.read())
                        
                        # Process the audio file
                        transcription = process_audio_file(temp_processing_path, "en")
                        
                        if transcription and not transcription.startswith("Error:"):
                            # Only send the transcription if it's different from the last one
                            if transcription != manager.last_transcription.get(client_id, ""):
                                logger.info(f"Sending transcription to client: {transcription[:50]}...")
                                await manager.send_transcription(client_id, transcription)
                                manager.last_transcription[client_id] = transcription
                            else:
                                logger.info(f"Skipping duplicate transcription")
                        else:
                            # If we get an error, send a more user-friendly message
                            error_msg = "Still listening..." if "Status code: 5" in transcription else transcription
                            logger.warning(f"Transcription error or empty: {transcription}")
                            if transcription == "":  # Only if truly empty, not for other errors
                                await manager.send_transcription(client_id, "Still listening...")
                            else:
                                await manager.send_transcription(client_id, error_msg)
                    except Exception as e:
                        logger.error(f"Error processing audio: {e}")
                        await manager.send_transcription(client_id, f"Processing error: {str(e)}")
                else:
                    logger.warning(f"Audio too short to process: {estimated_duration:.2f}s")
                    await manager.send_transcription(client_id, "Still listening...")
                
                # Update timing variables
                last_transcription_attempt = current_time
                manager.last_processed_time[client_id] = current_time
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for client {client_id}")
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"Error in websocket connection: {e}")
        try:
            await manager.send_transcription(client_id, f"Connection error: {str(e)}")
        except:
            pass
        manager.disconnect(client_id)

def process_audio_file(file_path: str, language: str = "en", retry_count=0):
    """
    Send audio file to the ASR API for transcription
    """
    processed_file_path = None
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return "Error: Audio file not found"
        
        # Get basic file info for logging
        file_size = os.path.getsize(file_path)
        logger.info(f"Processing audio file: {file_path} (size: {file_size} bytes)")
        
        # Skip processing if file is too small to contain meaningful audio
        if file_size < 1000:  # Less than 1KB
            logger.warning(f"File too small to process: {file_path} ({file_size} bytes)")
            return ""
        
        # Validate the audio file is actually a valid WAV file
        is_valid_wav = False
        try:
            with open(file_path, 'rb') as f:
                header = f.read(44)  # Read WAV header (minimum 44 bytes)
                # Check for basic WAV header signatures
                if header[0:4] == b'RIFF' and header[8:12] == b'WAVE':
                    is_valid_wav = True
                    logger.debug(f"Valid WAV file format confirmed for {file_path}")
                else:
                    logger.warning(f"File does not appear to be a valid WAV file: {file_path}")
        except Exception as e:
            logger.error(f"Error checking WAV header: {e}")
        
        # Check if audio format is supported and convert if needed
        if FFMPEG_AVAILABLE:
            try:
                # Try to convert to ensure it's in a format the ASR API can handle
                # Convert to 16kHz mono WAV if possible
                processed_file_path = ensure_required_format(file_path, sample_rate=16000, channels=1)
                if processed_file_path and processed_file_path != file_path:
                    logger.info(f"Converted audio format: {file_path} -> {processed_file_path}")
                    # Use the converted file
                    file_path = processed_file_path
            except Exception as e:
                logger.error(f"Error during audio conversion: {e}")
                # Continue with original file if conversion fails
        elif not is_valid_wav:
            logger.warning("FFmpeg not available and file may not be a valid WAV file. Processing may fail.")
        
        # Send to ASR API with appropriate timeouts for real-time processing
        with open(file_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {"language": language}
            
            try:
                logger.info(f"Sending request to ASR API: {ASR_API_URL}")
                # Use shorter timeout for real-time processing
                response = requests.post(ASR_API_URL, files=files, data=data, timeout=5)
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        transcription_text = result.get("transcription", "")
                        if transcription_text:
                            logger.info(f"Transcription received: {transcription_text[:50]}...")
                            return transcription_text
                        else:
                            logger.warning("Empty transcription received from API")
                            return ""
                    except Exception as e:
                        logger.error(f"Error parsing API response: {e}")
                        return f"Error parsing API response: {str(e)}"
                else:
                    logger.error(f"ASR API error: {response.status_code} - {response.text[:200]}...")
                    
                    # If server error and we haven't exceeded retry limit, try again
                    if response.status_code >= 500 and retry_count < MAX_API_RETRIES:
                        logger.info(f"Retrying API call ({retry_count + 1}/{MAX_API_RETRIES})")
                        time.sleep(0.5)  # Shorter wait before retrying for real-time results
                        return process_audio_file(file_path, language, retry_count + 1)
                    
                    return f"Error: Could not transcribe audio. Status code: {response.status_code}"
            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                
                # Retry on connection errors
                if retry_count < MAX_API_RETRIES:
                    logger.info(f"Retrying API call after connection error ({retry_count + 1}/{MAX_API_RETRIES})")
                    time.sleep(0.5)  # Shorter wait for real-time responsiveness
                    return process_audio_file(file_path, language, retry_count + 1)
                    
                return f"Connection error: {str(e)}"
                
    except Exception as e:
        logger.error(f"Error processing audio file: {e}")
        return f"Error: {str(e)}"
    finally:
        # Clean up any temporary converted files
        if FFMPEG_AVAILABLE and processed_file_path and processed_file_path != file_path:
            try:
                os.unlink(processed_file_path)
                logger.debug(f"Removed temporary converted file: {processed_file_path}")
            except Exception as e:
                logger.error(f"Error removing temporary converted file: {e}")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...), language: str = Form("en")):
    """
    Endpoint for direct file uploads (non-streaming)
    """
    # Generate a unique filename
    temp_file_name = f"upload_{uuid.uuid4()}.wav"
    temp_file_path = os.path.join(tempfile.gettempdir(), temp_file_name)
    
    try:
        # Save uploaded file to temp location
        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)
            logger.info(f"Saved uploaded file to {temp_file_path}")
        
        # Get file info
        file_size = os.path.getsize(temp_file_path)
        
        # Check if file is too small
        if file_size < 1000:  # Less than 1KB
            return {"transcription": "File too small to contain speech.", "warning": "File size too small"}
        
        # Process the file
        transcription = process_audio_file(temp_file_path, language)
        
        # Handle empty transcriptions
        if not transcription:
            return {"transcription": "No speech detected or transcription failed."}
        elif transcription.startswith("Error:"):
            return {"error": transcription, "transcription": "Transcription failed."}
            
        return {"transcription": transcription}
    except Exception as e:
        logger.error(f"Error in transcribe endpoint: {e}")
        return {"error": str(e), "transcription": "Transcription failed due to an error."}
    finally:
        # Ensure temp file is deleted even if an error occurs
        if os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
                logger.info(f"Removed temp file: {temp_file_path}")
            except Exception as e:
                logger.error(f"Error removing temp file: {e}")

if __name__ == "__main__":
    logger.info(f"FFmpeg available: {FFMPEG_AVAILABLE}")
    uvicorn.run("main:app", host="0.0.0.0", port=8484, reload=True) 