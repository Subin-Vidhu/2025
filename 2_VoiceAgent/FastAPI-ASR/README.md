# FastAPI Real-time Automatic Speech Recognition

A real-time ASR (Automatic Speech Recognition) application built with FastAPI, which uses an external ASR service for transcription.

## Features

- Real-time audio streaming from browser to server using WebSockets
- Audio processing and transcription via the canary.protosonline.in API
- **Smart hybrid approach**: Uses incremental processing with full-file fallback
- Simple and intuitive web interface with haptic feedback
- Support for multiple languages (depending on the API's capabilities)
- Direct file upload option for non-streaming transcription

## Recent Improvements

### Enhanced Real-time Processing
- **Adaptive hybrid approach:** Starts with incremental processing and falls back to full audio if needed
- **Sliding window technique:** Processes overlapping chunks to maintain context while minimizing API calls
- **Silence detection:** Avoids sending empty/silent audio chunks to the ASR API
- **Audio enhancement:** Applies audio filtering to improve transcription quality

### Browser-side Improvements
- **Optimized audio capture:** Custom audio settings for better ASR compatibility (mono, 16kHz)
- **Adaptive MIME type selection:** Automatically selects the best audio format for the browser
- **Smaller audio chunks:** Reduced from 1000ms to 500ms for more responsive feedback
- **Visual and haptic feedback:** Brief highlighting on transcript updates and vibration on mobile devices

## Architecture

This application follows a client-server architecture with a smart hybrid approach:

1. **Client (Browser)**: 
   - Captures high-quality audio (mono, 16kHz where possible)
   - Sends audio in small chunks (500ms) via WebSockets
   - Provides real-time visual and haptic feedback

2. **Server (FastAPI)**: 
   - **Sliding Window Approach:**
     - Stores individual audio chunks in separate files
     - Maintains a sliding window of recent chunks
     - Processes overlapping chunks to maintain context
   - **Hybrid Processing:**
     - Starts with incremental processing of chunks
     - Automatically switches to full-file approach after multiple empty results
     - Balances latency and accuracy adaptively
   - **Smart Audio Processing:**
     - Detects and skips silent audio
     - Applies audio filtering to enhance speech quality
     - Uses FFmpeg for optimal audio conversion when available
     - Falls back to manual WAV creation when needed

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

### Client-side
- Audio is captured in 500ms chunks for more responsive feedback
- AudioContext is used to enforce 16kHz mono audio when possible
- Adaptive MIME type selection based on browser capabilities
- Visual highlighting of transcription updates
- Haptic feedback (vibration) on mobile devices

### Server-side
- **Connection Management:**
  - Tracks processed and unprocessed audio chunks
  - Maintains unique client sessions with separate audio buffers
  - Handles WebSocket disconnects cleanly
  
- **Adaptive Processing:**
  - Sliding window approach with 10-chunk buffer (5 seconds of context)
  - Switches to full audio approach after 3 empty transcriptions
  - Overlapping chunks to maintain speech context
  
- **Audio Processing:**
  - Silence detection to avoid sending empty audio
  - Audio filtering (highpass/lowpass) to enhance speech quality
  - FFmpeg integration with fallback options
  - Manual WAV header generation when needed

## Performance Improvements

The application uses a series of optimization techniques:

1. **Hybrid processing approach:** 
   - Starts with incremental processing for low latency
   - Falls back to full audio for better accuracy when needed
   - Automatically adapts based on transcription results

2. **Intelligent chunk management:**
   - Individual chunks are stored separately
   - Sliding window provides sufficient context without overwhelming
   - Tracks processed/unprocessed chunks to avoid redundant processing

3. **Optimized audio processing:**
   - Silence detection avoids wasting API calls
   - Audio filtering enhances speech recognition quality
   - Smart retry logic for failed or empty transcriptions

4. **Browser optimizations:**
   - Shorter audio chunks (500ms) for more responsive feedback
   - Better audio format selection for transcription quality
   - Visual and haptic feedback for improved user experience

## Customization

You can customize this application by:

- Modifying the ASR API endpoint in `main.py`
- Adjusting the sliding window size (`chunk_buffer_size` in ConnectionManager)
- Tweaking the fallback threshold (`max_empty_transcriptions` in websocket_endpoint)
- Customizing the audio capture settings in the frontend
- Adding additional language support

## Limitations

- Requires an internet connection to access the external ASR service
- Audio quality and transcription accuracy may vary based on microphone quality and background noise
- Best performance is achieved when FFmpeg is installed
- Different browsers may provide different quality audio streams

## Troubleshooting

- If the application fails to start, ensure all dependencies are installed
- If no transcription appears, check browser console for WebSocket errors
- If transcriptions are empty but you hear audio, try switching to a different browser
- Ensure your microphone is properly connected and has necessary permissions
- For Firefox users: Enable the WebSocket protocol in your browser settings
- If you see "ffmpeg not found" warnings, install FFmpeg for better audio processing
- Check the server logs for any silent audio or processing errors
- Try increasing the sliding window size if transcriptions are fragmented

## License

This project is open-source and available under the MIT License. 