# FastAPI Real-time Automatic Speech Recognition

A real-time ASR (Automatic Speech Recognition) application built with FastAPI, which uses an external ASR service for transcription.

## Features

- Real-time audio streaming from browser to server using WebSockets
- Audio processing and transcription via the canary.protosonline.in API
- Simple and intuitive web interface
- Support for multiple languages (depending on the API's capabilities)
- Direct file upload option for non-streaming transcription

## Architecture

This application follows a client-server architecture:

1. **Client (Browser)**: Captures audio through the user's microphone and sends it in chunks to the server via WebSockets.
2. **Server (FastAPI)**: Processes incoming audio chunks, forwards them to the ASR API, and streams transcription results back to the client.
3. **External ASR Service**: Performs the actual speech recognition and returns the transcription.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser with microphone access

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

## Usage

1. Start the FastAPI server

```bash
python main.py
```

2. Open your web browser and navigate to:

```
http://localhost:8000
```

3. Use the web interface to:
   - Select your preferred language
   - Click "Start Recording" to begin capturing audio
   - View real-time transcription results
   - Click "Stop" when finished

## API Endpoints

- `GET /`: Returns a status message indicating the API is running
- `WebSocket /ws/{client_id}`: WebSocket endpoint for real-time audio streaming and transcription
- `POST /transcribe/`: HTTP endpoint for direct file uploads (supports form data with 'file' and 'language' fields)

## Technical Details

- Audio is captured and streamed in 1-second chunks
- WebSockets are used for bidirectional communication
- Temporary files are used to store audio chunks before processing
- The external ASR API is called with form-data containing the audio file and language code

## Customization

You can customize this application by:

- Modifying the ASR API endpoint in `main.py`
- Adding support for additional languages in the frontend
- Adjusting the chunk size for audio processing
- Implementing authentication for API access

## Limitations

- Requires an internet connection to access the external ASR service
- Audio quality and transcription accuracy may vary based on microphone quality and background noise
- The external ASR service might have usage limits or require API keys

## Troubleshooting

- If the application fails to start, ensure all dependencies are installed
- If no transcription appears, check browser console for WebSocket errors
- Ensure your microphone is properly connected and has necessary permissions
- For Firefox users: Enable the WebSocket protocol in your browser settings

## License

This project is open-source and available under the MIT License. 