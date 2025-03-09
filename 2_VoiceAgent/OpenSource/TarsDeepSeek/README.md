# **TARS - Voice AI Assistant using DeepSeek R1**
This project is a real-time voice AI assistant named TARS, powered by DeepSeek R1 via Ollama. It uses speech\_recognition for speech-to-text conversion and pyttsx3 for text-to-speech
## **Features**
• Real-time speech recognition using speech\_recognition.

• AI-powered responses from DeepSeek R1 (7B model) via Ollama.

• Text-to-speech conversion using pyttsx3 for a robotic voice.

• Fully offline transcription and speech synthesis (no external API keys needed).
## **Prerequisites**
### **Install Dependencies**
Run the following command to install required Python libraries:
> *pip install speechrecognition pyttsx3 ollama*
### **Install PortAudio (Required for SpeechRecognition)**
• Debian/Ubuntu:
> `  `*sudo apt install portaudio19-dev*

• MacOS:
> `  `*brew install portaudio*
• Windows:
> `works with the default python installation, no need to install extra dependencies`
### **Download DeepSeek R1 Model**
Since this script uses DeepSeek R1 via Ollama, install Ollama and pull the model:
> *ollama pull deepseek-r1:7b*
## **Usage**
Run the script to start TARS:
> *python deepseek_tars.py*
### **How It Works**
1\. Listens to user speech and converts it into text.

2\. Sends text to DeepSeek R1 via Ollama to generate an AI response.

3\. Speaks the response back to the user using pyttsx3.

To exit, say 'exit', 'quit', or 'bye'.
## **Customization**
• Change AI personality: Modify the system message inside self.full\_transcript in the script.

• Adjust voice properties: Modify pyttsx3 settings to change speed, volume, and voice type.

• Use different AI models: Replace 'deepseek-r1:7b' with any other Ollama-compatible model.
## **Notes**
• No API keys are required, making it fully offline for transcription and speech synthesis.

• Accuracy may vary for speech recognition based on background noise and microphone quality.
## **License**
This project is open-source and free to use. 🚀
