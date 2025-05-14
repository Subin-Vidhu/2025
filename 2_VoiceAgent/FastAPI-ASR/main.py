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
        
        # New fields for incremental processing
        self.processed_chunks = {}  # Track which chunks have been processed
        self.unprocessed_chunks = {}  # Track chunks waiting to be processed
        self.chunk_timestamps = {}  # Track when chunks were received
        self.chunk_buffer_size = 10  # Increased from 3 to 10 to include more context
        self.sliding_window_chunks = {}  # Store chunks in the current sliding window

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.temp_audio_files[client_id] = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        self.temp_chunk_files[client_id] = []  # Initialize empty list for chunk files
        self.last_processed_time[client_id] = time.time()
        self.audio_data[client_id] = bytearray()  # Initialize empty bytearray for audio data
        self.last_transcription[client_id] = ""  # Initialize last transcription to empty string
        self.chunk_counter[client_id] = 0  # Initialize chunk counter
        
        # Initialize new fields for incremental processing
        self.processed_chunks[client_id] = []
        self.unprocessed_chunks[client_id] = []
        self.chunk_timestamps[client_id] = {}
        self.sliding_window_chunks[client_id] = []
        
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
            
        # Clean up all tracking data
        for attr in [
            'last_processed_time', 'audio_data', 'last_transcription', 
            'chunk_counter', 'processed_chunks', 'unprocessed_chunks', 
            'chunk_timestamps', 'sliding_window_chunks'
        ]:
            container = getattr(self, attr)
            if client_id in container:
                del container[client_id]
            
        logger.info(f"Client {client_id} disconnected")

    async def send_transcription(self, client_id: str, message: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(message)
            
    async def add_chunk(self, client_id: str, audio_data: bytes):
        """
        Add a new audio chunk for the client and return a unique identifier for it
        """
        # Save chunk to a separate file
        chunk_id = f"{client_id}_{self.chunk_counter.get(client_id, 0)}"
        self.chunk_counter[client_id] = self.chunk_counter.get(client_id, 0) + 1
        
        # Create temp file for this chunk
        chunk_path = os.path.join(
            tempfile.gettempdir(),
            f"chunk_{chunk_id}_{int(time.time())}.raw"
        )
        
        # Write the raw audio data to file
        with open(chunk_path, "wb") as chunk_file:
            chunk_file.write(audio_data)
        
        # Track the chunk
        self.unprocessed_chunks[client_id].append(chunk_path)
        self.chunk_timestamps[client_id][chunk_path] = time.time()
        self.temp_chunk_files[client_id].append(chunk_path)
        
        # Also append to the full recording file for backup/complete transcription
        if client_id in self.temp_audio_files:
            self.temp_audio_files[client_id].write(audio_data)
            self.temp_audio_files[client_id].flush()
        
        return chunk_path
        
    def get_chunks_to_process(self, client_id: str):
        """
        Get a list of chunk files that should be processed in the current window
        """
        if client_id not in self.unprocessed_chunks or not self.unprocessed_chunks[client_id]:
            return []
            
        # Get most recent N chunks for the sliding window
        window_size = min(self.chunk_buffer_size, len(self.unprocessed_chunks[client_id]))
        return self.unprocessed_chunks[client_id][-window_size:]
        
    def mark_chunks_as_processed(self, client_id: str, chunk_paths):
        """
        Mark the specified chunks as processed
        """
        if client_id not in self.unprocessed_chunks:
            return
            
        for chunk in chunk_paths:
            if chunk in self.unprocessed_chunks[client_id]:
                self.unprocessed_chunks[client_id].remove(chunk)
                self.processed_chunks[client_id].append(chunk)
                
    def get_sliding_window_file(self, client_id: str, chunk_paths):
        """
        Create a WAV file containing the audio from the specified chunks
        """
        if not chunk_paths:
            return None
            
        # Create a temporary WAV file for the sliding window
        window_fd, window_path = tempfile.mkstemp(suffix=".wav")
        os.close(window_fd)
        self.temp_chunk_files[client_id].append(window_path)
        
        # If FFmpeg is available, use it to create a proper WAV file
        if FFMPEG_AVAILABLE:
            # Create a file with raw concatenated audio
            raw_fd, raw_path = tempfile.mkstemp(suffix=".raw")
            os.close(raw_fd)
            self.temp_chunk_files[client_id].append(raw_path)
            
            # Concatenate the raw audio chunks
            with open(raw_path, "wb") as raw_file:
                for chunk_path in chunk_paths:
                    with open(chunk_path, "rb") as chunk_file:
                        raw_file.write(chunk_file.read())
            
            # Use FFmpeg to convert the raw audio to WAV with specific settings for ASR
            try:
                cmd = [
                    "ffmpeg",
                    "-f", "s16le",  # 16-bit PCM
                    "-ar", "16000",  # 16kHz sample rate
                    "-ac", "1",      # Mono
                    "-i", raw_path,
                    "-af", "highpass=f=200,lowpass=f=3000,areverse,silenceremove=start_periods=1:start_silence=0.1:start_threshold=-50dB,areverse",  # Audio filtering to remove noise
                    "-sample_fmt", "s16",  # 16-bit samples
                    "-y",            # Overwrite output
                    window_path
                ]
                
                process = subprocess.run(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if process.returncode != 0:
                    logger.error(f"FFmpeg error: {process.stderr}")
                    
                    # Fallback to simpler conversion if the filters cause problems
                    cmd = [
                        "ffmpeg",
                        "-f", "s16le",  # 16-bit PCM
                        "-ar", "16000",  # 16kHz sample rate
                        "-ac", "1",      # Mono
                        "-i", raw_path,
                        "-y",            # Overwrite output
                        window_path
                    ]
                    
                    process = subprocess.run(
                        cmd, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    if process.returncode != 0:
                        logger.error(f"FFmpeg fallback error: {process.stderr}")
                        return None
                
                # Check if the output file exists and has reasonable size
                if os.path.exists(window_path) and os.path.getsize(window_path) > 1000:  # Ensure it's big enough
                    logger.info(f"Successfully created sliding window file: {window_path}")
                    return window_path
                else:
                    logger.error(f"Created file is too small: {window_path}")
                    return None
                    
            except Exception as e:
                logger.error(f"Error creating sliding window file: {e}")
                return None
        else:
            # Without FFmpeg, try to create a basic WAV file manually
            try:
                # Create a WAV header
                sample_rate = 16000
                channels = 1
                bits_per_sample = 16
                
                # Calculate total data size
                data_size = 0
                for chunk_path in chunk_paths:
                    data_size += os.path.getsize(chunk_path)
                
                # Create header
                wav_header = bytearray()
                # RIFF header
                wav_header.extend(b'RIFF')
                wav_header.extend((data_size + 36).to_bytes(4, byteorder='little'))  # File size - 8
                wav_header.extend(b'WAVE')
                # fmt chunk
                wav_header.extend(b'fmt ')
                wav_header.extend((16).to_bytes(4, byteorder='little'))  # fmt chunk size
                wav_header.extend((1).to_bytes(2, byteorder='little'))   # PCM format
                wav_header.extend((channels).to_bytes(2, byteorder='little'))
                wav_header.extend((sample_rate).to_bytes(4, byteorder='little'))
                wav_header.extend((sample_rate * channels * bits_per_sample // 8).to_bytes(4, byteorder='little'))  # Byte rate
                wav_header.extend((channels * bits_per_sample // 8).to_bytes(2, byteorder='little'))  # Block align
                wav_header.extend((bits_per_sample).to_bytes(2, byteorder='little'))
                # data chunk
                wav_header.extend(b'data')
                wav_header.extend((data_size).to_bytes(4, byteorder='little'))
                
                # Write header and audio data
                with open(window_path, "wb") as wav_file:
                    wav_file.write(wav_header)
                    for chunk_path in chunk_paths:
                        with open(chunk_path, "rb") as chunk_file:
                            wav_file.write(chunk_file.read())
                
                return window_path
                
            except Exception as e:
                logger.error(f"Error creating WAV file manually: {e}")
                return None

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
        transcription_interval = 1.0  # seconds - even shorter interval for more responsive transcription
        min_chunk_duration = 1.0  # Increased from 0.5 to 1.0 seconds for better results
        
        # Track transcription state
        current_transcription = ""
        empty_transcription_count = 0
        max_empty_transcriptions = 3  # Switch to full file approach after this many empty results
        using_full_file = False  # Whether we've switched to the full file approach
        
        while True:
            # Receive binary audio data from client
            data = await websocket.receive_bytes()
            
            # Add the chunk to our tracking system
            chunk_path = await manager.add_chunk(client_id, data)
            accumulated_size += len(data)
            
            # Only attempt transcription at intervals to avoid overwhelming the server
            current_time = time.time()
            elapsed_since_last_transcription = current_time - last_transcription_attempt
            
            # Process audio periodically 
            if elapsed_since_last_transcription > transcription_interval:
                # Check if we should use the full file approach
                if empty_transcription_count >= max_empty_transcriptions:
                    using_full_file = True
                
                transcription = ""
                
                if using_full_file:
                    # Use the full audio file approach (like the original code)
                    try:
                        # Get the current size of the accumulated audio
                        file_size = temp_file.tell()
                        
                        # Estimate duration
                        estimated_duration = file_size / (16000 * 2)
                        
                        logger.info(f"Using full file approach for client {client_id} - Size: {file_size} bytes, Est. duration: {estimated_duration:.2f}s")
                        
                        if estimated_duration >= min_chunk_duration:
                            # Make a copy of the temp file to avoid conflicts
                            temp_processing_path = os.path.join(
                                tempfile.gettempdir(),
                                f"processing_{client_id}_{int(current_time)}.wav"
                            )
                            
                            # Add to list of temp files to clean up later
                            manager.temp_chunk_files[client_id].append(temp_processing_path)
                            
                            # Copy the file for processing
                            with open(temp_file.name, 'rb') as src, open(temp_processing_path, 'wb') as dst:
                                dst.write(src.read())
                            
                            # Process the full audio file
                            transcription = process_chunk(temp_processing_path, "en", is_incremental=False)
                    except Exception as e:
                        logger.error(f"Error processing full audio file: {e}")
                else:
                    # Try the sliding window approach
                    try:
                        # Get chunks to process in the current sliding window
                        chunks_to_process = manager.get_chunks_to_process(client_id)
                        
                        if chunks_to_process:
                            # Create a WAV file with the current window of chunks
                            window_path = manager.get_sliding_window_file(client_id, chunks_to_process)
                            
                            if window_path:
                                # Get window file size
                                window_size = os.path.getsize(window_path)
                                
                                # Estimate duration
                                estimated_duration = window_size / (16000 * 2)
                                
                                logger.info(f"Processing sliding window for client {client_id} - Size: {window_size} bytes, Est. duration: {estimated_duration:.2f}s")
                                
                                # Only process if we have enough audio data
                                if estimated_duration >= min_chunk_duration:
                                    # Process the audio window
                                    transcription = process_chunk(window_path, "en")
                                    
                                    # Mark the processed chunks (except the most recent ones to maintain overlap)
                                    if len(chunks_to_process) > 2:  # Keep more recent chunks in the window
                                        manager.mark_chunks_as_processed(client_id, chunks_to_process[:-2])
                                else:
                                    logger.warning(f"Audio window too short to process: {estimated_duration:.2f}s")
                            else:
                                logger.error(f"Failed to create sliding window file for client {client_id}")
                        else:
                            logger.warning(f"No unprocessed chunks available for client {client_id}")
                    except Exception as e:
                        logger.error(f"Error processing audio chunks: {e}")
                
                # Handle the transcription result
                if transcription and not transcription.startswith("Error:"):
                    # Reset the empty transcription counter
                    empty_transcription_count = 0
                    
                    # Only send the transcription if it's different from the last one
                    if transcription != manager.last_transcription.get(client_id, ""):
                        logger.info(f"Sending transcription to client: {transcription[:50]}...")
                        await manager.send_transcription(client_id, transcription)
                        manager.last_transcription[client_id] = transcription
                    else:
                        logger.info(f"Skipping duplicate transcription")
                else:
                    # Increment empty transcription counter
                    if not transcription or transcription == "":
                        empty_transcription_count += 1
                        logger.warning(f"Empty transcription count: {empty_transcription_count}/{max_empty_transcriptions}")
                    
                    # Send appropriate message for errors or empty transcriptions
                    error_msg = "Still listening..." if not transcription or transcription == "" or "Status code: 5" in transcription else transcription
                    logger.warning(f"Transcription error or empty: {transcription}")
                    await manager.send_transcription(client_id, error_msg)
                
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

def process_chunk(file_path: str, language: str = "en", retry_count=0, is_incremental=True):
    """
    Process a single audio chunk
    
    Args:
        file_path: Path to the audio file
        language: Language code for transcription
        retry_count: Current retry attempt (for internal use)
        is_incremental: Whether this is part of an incremental transcription
        
    Returns:
        Transcription text or error message
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
        
        # Validate the audio file format
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
        
        # Analyze audio for silence - if it's just silence, skip API call
        if FFMPEG_AVAILABLE:
            try:
                # Use FFmpeg to detect silence
                cmd = [
                    "ffmpeg",
                    "-i", file_path,
                    "-af", "silencedetect=noise=-50dB:d=0.5",
                    "-f", "null",
                    "-"
                ]
                process = subprocess.run(
                    cmd, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                # Check if the entire file is silence
                if "silence_end" not in process.stderr and "silence_start" in process.stderr:
                    logger.warning(f"Audio file appears to be all silence: {file_path}")
                    return ""
            except Exception as e:
                logger.error(f"Error analyzing audio for silence: {e}")
        
        # Send to ASR API with appropriate timeouts
        with open(file_path, "rb") as audio_file:
            files = {"file": audio_file}
            data = {
                "language": language,
            }
            
            # Add incremental flag if supported by API
            if is_incremental:
                data["incremental"] = "true"
            
            try:
                logger.info(f"Sending request to ASR API: {ASR_API_URL}")
                # Use shorter timeout for real-time processing
                response = requests.post(ASR_API_URL, files=files, data=data, timeout=5)
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        transcription_text = result.get("transcription", "")
                        
                        # Handle empty response intelligently
                        if not transcription_text:
                            # Log the empty response
                            logger.warning("Empty transcription received from API")
                            
                            # For non-incremental processing or if we've already retried, return empty
                            if not is_incremental or retry_count > 0:
                                return ""
                                
                            # For incremental processing and first attempt, retry once with non-incremental mode
                            logger.info("Retrying with non-incremental mode")
                            return process_chunk(file_path, language, retry_count + 1, is_incremental=False)
                        else:
                            logger.info(f"Transcription received: {transcription_text[:50]}...")
                            return transcription_text
                    except Exception as e:
                        logger.error(f"Error parsing API response: {e}")
                        return f"Error parsing API response: {str(e)}"
                else:
                    logger.error(f"ASR API error: {response.status_code} - {response.text[:200]}...")
                    
                    # If server error and we haven't exceeded retry limit, try again
                    if response.status_code >= 500 and retry_count < MAX_API_RETRIES:
                        logger.info(f"Retrying API call ({retry_count + 1}/{MAX_API_RETRIES})")
                        time.sleep(0.5)  # Shorter wait before retrying for real-time results
                        return process_chunk(file_path, language, retry_count + 1, is_incremental)
                    
                    if response.status_code == 413:  # Payload too large
                        return "Error: Audio file too large for API"
                    
                    return f"Error: Could not transcribe audio. Status code: {response.status_code}"
            except requests.RequestException as e:
                logger.error(f"Request error: {e}")
                
                # Retry on connection errors
                if retry_count < MAX_API_RETRIES:
                    logger.info(f"Retrying API call after connection error ({retry_count + 1}/{MAX_API_RETRIES})")
                    time.sleep(0.5)  # Shorter wait for real-time responsiveness
                    return process_chunk(file_path, language, retry_count + 1, is_incremental)
                    
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
        
        # Process the file - not incremental for one-time uploads
        transcription = process_chunk(temp_file_path, language, is_incremental=False)
        
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