import gradio as gr
from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()

client = OpenAI(
    organization=os.environ.get('ORG_ID'),
    project=os.environ.get('PROJECT_ID')
)

def chatbot(user_input, history):
    messages = []
    
    # Correct way to handle Gradio chat history
    for message in history:
        messages.append({"role": "user", "content": message[0]})
        messages.append({"role": "assistant", "content": message[1]})
    
    # Add current message
    messages.append({"role": "user", "content": user_input})
    
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )
    
    response = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:  # Check if content exists
            response += chunk.choices[0].delta.content  # Use delta.content instead of text
            yield response

# Create Gradio interface
demo = gr.ChatInterface(
    fn=chatbot, 
    title="OpenAI Chatbot", 
    description="Chat with OpenAI's language model",
)

# Launch Gradio app
demo.launch()