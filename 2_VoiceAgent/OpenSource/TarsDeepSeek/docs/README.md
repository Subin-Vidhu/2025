# TARS Voice Agent Developer Documentation

## Overview
TARS Voice Agent is an interactive AI-powered voice assistant that can engage in conversations using speech recognition and text-to-speech capabilities. The agent uses local LLM (Language Learning Model) inference through Ollama with the DeepSeek model for generating responses.

## Dependencies
- `ollama`: Local LLM inference engine
- `pyttsx3`: Text-to-speech conversion library
- `speech_recognition`: Library for performing speech recognition

## Installation
```bash
pip install ollama-python pyttsx3 SpeechRecognition pyaudio
```

Note: You'll need to have Ollama installed and the DeepSeek model pulled:
```bash
# Install Ollama from https://ollama.ai/
# Pull the DeepSeek model
ollama pull deepseek-r1:7b
```

## Class: AIVoiceAgent

### Initialization
```python
agent = AIVoiceAgent()
```
During initialization, the agent:
1. Sets up the text-to-speech engine (pyttsx3)
2. Configures voice properties (rate, volume, voice type)
3. Initializes the speech recognizer
4. Sets up the conversation history with a system prompt

### Key Methods

#### 1. listen_to_user()
Listens for user input through the microphone and converts speech to text.

```python
user_input = agent.listen_to_user()
```

Features:
- Adjusts for ambient noise
- Uses Google's speech recognition service
- Handles recognition errors gracefully
- Returns None if speech cannot be recognized

#### 2. generate_ai_response(user_text)
Generates an AI response using the Ollama/DeepSeek model and speaks it.

```python
agent.generate_ai_response("Tell me a joke")
```

Process:
1. Adds user input to conversation history
2. Sends request to Ollama with DeepSeek model
3. Processes and speaks the response
4. Updates conversation history

#### 3. start_chat()
Main loop that handles the conversation flow.

```python
agent.start_chat()
```

Features:
- Continuous listening loop
- Exit commands ("exit", "quit", "bye")
- Error handling for failed speech recognition

## Example Usage

```python
from deepseek_tars import AIVoiceAgent

# Create an instance of the voice agent
agent = AIVoiceAgent()

# Start the conversation
agent.start_chat()
```

## Test Cases

```python
def test_voice_agent():
    agent = AIVoiceAgent()
    
    # Test 1: Basic Response Generation
    response = agent.generate_ai_response("What is 2+2?")
    assert response is not None
    
    # Test 2: Exit Commands
    test_inputs = ["exit", "quit", "bye"]
    for input in test_inputs:
        # Should gracefully exit
        assert input.lower() in ["exit", "quit", "bye"]
    
    # Test 3: Conversation History
    agent.generate_ai_response("Hello")
    assert len(agent.full_transcript) >= 3  # System prompt + user + assistant
```

## Troubleshooting

1. **Speech Recognition Issues**
   - Ensure microphone permissions are granted
   - Check internet connection (required for Google Speech Recognition)
   - Adjust microphone volume and positioning

2. **Ollama Issues**
   - Verify Ollama is running locally
   - Ensure DeepSeek model is properly pulled
   - Check Ollama logs for any errors

3. **Text-to-Speech Issues**
   - Verify audio output device is working
   - Check system volume settings
   - Try different voices if speech is unclear

## Limitations

1. Requires internet connection for speech recognition
2. Response length limited to 300 characters
3. Uses Google Speech Recognition API which may have usage limits
4. Requires local GPU for optimal Ollama performance

## Future Improvements

1. Add support for offline speech recognition
2. Implement multiple language support
3. Add voice selection options
4. Improve error handling and recovery
5. Add conversation logging
6. Implement configurable response length

## Security Considerations

1. Speech data is sent to Google's servers for recognition
2. Local LLM inference provides privacy for responses
3. No data persistence implemented
4. No authentication mechanism in place

## Contributing

When contributing to this project:
1. Follow the existing code style
2. Add appropriate error handling
3. Update documentation for new features
4. Add test cases for new functionality
5. Test with different operating systems and configurations 