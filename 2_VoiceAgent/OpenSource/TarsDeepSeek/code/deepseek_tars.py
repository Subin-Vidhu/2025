import ollama
import pyttsx3  
import speech_recognition as sr  

class AIVoiceAgent:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  

        self.full_transcript = [
            {"role": "system", "content": "You are a robot called AIRA created by Aramis Imaging. Answer questions in less than 300 characters."},
        ]

    def listen_to_user(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.5)
            audio = self.recognizer.listen(source)
            
            try:
                print("Recognizing...")
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Sorry, I didn't understand that.")
                return None
            except sr.RequestError:
                print("Sorry, I'm having trouble accessing the speech recognition service.")
                return None

    def generate_ai_response(self, user_text):
        self.full_transcript.append({"role": "user", "content": user_text})
        print(f"\nUser: {user_text}")

        ollama_response = ollama.chat(
            model="deepseek-r1:7b",
            messages=self.full_transcript
        )

        ai_text = ollama_response["message"]["content"].strip()
        print("TARS:", ai_text)

        self.engine.say(ai_text)
        self.engine.runAndWait()
        
        self.full_transcript.append({"role": "assistant", "content": ai_text})

    def start_chat(self):
        print("Hello! I'm TARS. How can I assist you today?")
        while True:
            user_input = self.listen_to_user()
            
            if user_input is None:
                continue
            
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("TARS: Goodbye!")
                self.engine.say("Goodbye!")
                self.engine.runAndWait()
                break
            
            self.generate_ai_response(user_input)

ai_voice_agent = AIVoiceAgent()
ai_voice_agent.start_chat()