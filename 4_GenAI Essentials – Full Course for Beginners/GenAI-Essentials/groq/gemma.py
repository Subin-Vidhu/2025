from groq import Groq
import os
import dotenv
dotenv.load_dotenv()

client = Groq()
completion = client.chat.completions.create(
    model="gemma2-9b-it",
    messages=[{"role": "user", "content": "Hello, how are you today?"}],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
