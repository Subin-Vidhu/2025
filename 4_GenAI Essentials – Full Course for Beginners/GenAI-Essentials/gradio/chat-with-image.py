import gradio as gr
from openai import OpenAI
import os
import dotenv
dotenv.load_dotenv()

client = OpenAI(
  organization=os.environ.get('ORG_ID'),
  project=os.environ.get('PROJECT_ID')
)

def generate_image(prompt):
  """Generate an image using DALL-E"""
  try:
    response = client.images.generate(
      model="dall-e-3",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )
    return response.data[0].url
  except Exception as e:
    print(f"Image generation error: {e}")
    return None

def chat_and_generate(user_input, history):
  messages = []
  
  # Handle history
  for message in history:
    messages.append({"role": "user", "content": message[0]})
    messages.append({"role": "assistant", "content": message[1]})
  
  messages.append({"role": "user", "content": user_input})
  
  # Get chat response
  stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    stream=True,
  )
  
  response = ""
  for chunk in stream:
    if chunk.choices[0].delta.content is not None:
      response += chunk.choices[0].delta.content
  
  # Generate image based on response
  image_url = generate_image(response)
  
  return response, image_url

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=1):
          image_output = gr.Image(label="Generated Image")
        with gr.Column(scale=1):
          chatbot = gr.Chatbot()
          msg = gr.Textbox(label="Message")
          #clear = gr.Button("Clear")
    
    def respond(message, chat_history):
      response, image_url = chat_and_generate(message, chat_history)
      chat_history.append((message, response))
      return "", chat_history, image_url

    msg.submit(respond, [msg, chatbot], [msg, chatbot, image_output])
    clear.click(lambda: None, None, chatbot)

if __name__ == "__main__":
  demo.launch()