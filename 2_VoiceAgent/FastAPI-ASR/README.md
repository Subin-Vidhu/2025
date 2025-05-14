# FastAPI Real-time Automatic Speech Recognition

A real-time ASR (Automatic Speech Recognition) application built with FastAPI, which uses an external ASR service for transcription.

## Features

- Real-time audio streaming from browser to server using WebSockets
- Audio processing and transcription via the canary.protosonline.in API
- **True incremental audio processing - only new audio chunks are sent to ASR API**
- Simple and intuitive web interface
- Support for multiple languages (depending on the API's capabilities)
- Direct file upload option for non-streaming transcription

## Recent Improvements

### Audio Processing Enhancements
- **True incremental processing:** Only new audio chunks are processed, not the entire recording
- **Custom WAV header generation:** Creates properly formatted audio files for each chunk
- **Fixed WAV header issues:** Now properly handles audio chunks with correct WAV headers
- **Improved FFmpeg integration:** Better error handling and recovery when audio conversion fails
- **Audio format validation:** Validates audio files before processing to prevent errors
- **Robust error handling:** Gracefully handles malformed audio data with detailed diagnostics

## Architecture

This application follows a client-server architecture:

1. **Client (Browser)**: Captures audio through the user's microphone and sends it in chunks to the server via WebSockets.
2. **Server (FastAPI)**: 
   - Processes incoming audio chunks using an efficient true incremental approach
   - Only extracts, formats, and processes the new audio since the last transcription attempt
   - Creates proper WAV files on-the-fly with correct headers
   - Streams transcription results back to the client in real-time
3. **External ASR Service**: Performs the actual speech recognition and returns the transcription.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser with microphone access
- **FFmpeg** (recommended for optimal audio processing, but optional)

## Installation

1. Clone the repository or extract files to your local machine
2. Navigate to the project directory

```bash
cd 2_VoiceAgent/FastAPI-ASR
```

3. Install the required dependencies

```bash
pip install -r requirements.txt
```

4. (Optional but recommended) Install FFmpeg:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg` or equivalent

## Usage

1. Start the FastAPI server

```bash
python main.py
```

2. Open your web browser and navigate to:

```
http://localhost:8484
```

3. Use the web interface to:
   - Select your preferred language
   - Click "Start Recording" to begin capturing audio
   - View real-time transcription results
   - Click "Stop" when finished

## API Endpoints

- `GET /`: Returns the web interface
- `GET /api/status`: Returns the status of the API and external services
- `WebSocket /ws/{client_id}`: WebSocket endpoint for real-time audio streaming and transcription
- `POST /transcribe/`: HTTP endpoint for direct file uploads (supports form data with 'file' and 'language' fields)

## Technical Details

- Audio is captured and streamed in 1-second chunks (~49KB each)
- The server processes **only new audio data** for each transcription attempt
- Each audio chunk is provided with proper WAV headers for compatibility
- Temporary files for audio chunks are automatically cleaned up
- Audio format conversion is performed as needed (when FFmpeg is available)
- Connection and error handling is robust with automatic retries

## Performance Improvements

The application has been optimized to:

1. **Process only new audio chunks**: Instead of re-processing the entire recording each time, only new audio data is sent to the ASR API
2. **Generate WAV headers dynamically**: Creates valid audio files on-the-fly without requiring FFmpeg for basic operations
3. **Clean up temporary files**: All temporary files are properly managed and removed after processing
4. **Support audio format conversion**: When FFmpeg is available, audio is converted to optimal format for the ASR API
5. **Handle network issues gracefully**: Automatic retries for network failures with the ASR API
6. **Provide meaningful error messages**: Better error handling and user feedback

## Customization

You can customize this application by:

- Modifying the ASR API endpoint in `main.py`
- Adjusting the chunk processing parameters for audio
- Implementing authentication for API access
- Adding additional language support

## Limitations

- Requires an internet connection to access the external ASR service
- Audio quality and transcription accuracy may vary based on microphone quality and background noise
- The external ASR service might have usage limits or require API keys
- Best performance is achieved when FFmpeg is installed

## Troubleshooting

- If the application fails to start, ensure all dependencies are installed
- If no transcription appears, check browser console for WebSocket errors
- Ensure your microphone is properly connected and has necessary permissions
- For Firefox users: Enable the WebSocket protocol in your browser settings
- If you see "ffmpeg not found" warnings, install FFmpeg for better audio processing
- If audio processing errors occur, check that your FFmpeg installation is working correctly
- For Windows users: Ensure FFmpeg is properly added to your PATH environment variable

## License

This project is open-source and available under the MIT License. 