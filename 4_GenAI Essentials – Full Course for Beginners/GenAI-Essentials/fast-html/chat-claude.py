from fasthtml.common import *
from openai import OpenAI
from markdown import markdown
import os
import dotenv
dotenv.load_dotenv()


app, rt = fast_app()
client = OpenAI(
  organization=os.environ.get('ORG_ID'),
  project=os.environ.get('PROJECT_ID')
)

chat_histories = {}

def format_message(content, cls):
    html_content = markdown(content)
    return Div(NotStr(html_content), cls=f"message {cls}")

@rt("/")
def get():
    return Titled("Chat with GPT-4", 
        Div(
            Div(id="chat-messages", cls="messages"),
            Form(
                Input(id="user-input", name="message", placeholder="Type your message..."),
                Button("Send", type="submit"),
                hx_post="/chat",
                hx_target="#chat-messages",
                hx_swap="beforeend"
            ),
            Style("""
                .messages { height: 400px; overflow-y: auto; border: 1px solid #ccc; padding: 1rem; margin-bottom: 1rem; }
                .message { margin-bottom: 0.5rem; padding: 0.5rem; border-radius: 4px; }
                .message p { margin: 0; }
                .message pre { background: #f8f8f8; padding: 0.5rem; border-radius: 4px; overflow-x: auto; }
                .message code { background: #f8f8f8; padding: 0.2rem 0.4rem; border-radius: 2px; }
                .user-message { background: #e3f2fd; margin-left: 20%; }
                .assistant-message { background: #f5f5f5; margin-right: 20%; }
            """)
        )
    )

@rt("/chat")
def post(message: str, session):
    chat_id = session.get("chat_id")
    if not chat_id:
        chat_id = str(len(chat_histories))
        session["chat_id"] = chat_id
        
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
    chat_histories[chat_id].append({"role": "user", "content": message})
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=150,
        messages=chat_histories[chat_id]
    )
    
    assistant_message = response.choices[0].message.content
    chat_histories[chat_id].append({"role": "assistant", "content": assistant_message})
    
    return (
        format_message(message, "user-message"),
        format_message(assistant_message, "assistant-message"),
        Input(id="user-input", value="", hx_swap_oob="true")
    )

serve()