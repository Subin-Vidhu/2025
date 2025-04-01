# ai_chat_image_app.py
import os
import dotenv
dotenv.load_dotenv()

import requests
from io import BytesIO
from fasthtml.common import *


from openai import OpenAI
# 1) Instantiate your OpenAI client
client = OpenAI(
    organization=os.environ.get("ORG_ID"),
    project=os.environ.get("PROJECT_ID"),
    api_key=os.environ.get("OPENAI_API_KEY")  # optional if you want
)


# 2) Build a FastHTML app using fast_app (which sets up sessions, debugging, etc.)
app, rt = fast_app(debug=True)


# 3) Our main route handles BOTH GET and POST
#    - GET: show the 2-column layout with the current image + chat messages + form
#    - POST: user typed a new prompt => process chat & image, then redirect
@rt("/")
def getpost(sess, prompt: str = None):
    """
    The `prompt` param is optional. If provided (i.e. this is a POST),
    we'll do the chat & image generation. Then we redirect to GET.
    """
    # Initialize session keys if missing
    if "messages" not in sess: sess["messages"] = []
    if "image_url" not in sess: sess["image_url"] = None

    # If prompt is provided => POST => handle chat + image generation
    if prompt is not None:
        # 1) Add user message
        sess["messages"].append({"role": "user", "content": prompt})

        # 2) Send entire conversation to the GPT-4o-mini style model
        #    (As per your snippet: client.chat.completions.create)
        try:
            chat_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=sess["messages"],
                max_tokens=150
            )
            response_text = chat_response["choices"][0]["message"]["content"]
            # 3) Add assistant's response
            sess["messages"].append({"role": "assistant", "content": response_text})
        except Exception as e:
            # If error in chat completion
            sess["messages"].append({"role": "assistant", "content": f"**Error**: {str(e)}"})

        # 4) Generate an image with DALL·E 3 from the user’s prompt
        #    (As per your snippet: client.images.generate)
        try:
            enhanced_prompt = f"High quality, detailed image of: {prompt}"
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            new_url = image_response["data"][0]["url"]
            sess["image_url"] = new_url
        except Exception as e:
            # If error in image generation
            sess["image_url"] = None
            # We'll let the chat show that error as a message
            sess["messages"].append({"role": "assistant", "content": f"**Image Error**: {str(e)}"})

        # 5) Now that we've updated session with new messages + image, 
        #    do a redirect so refreshing doesn't re-send the form.
        return RedirectResponse("/", status_code=303)


    # ========== If we reach here, it's a GET request. ==========

    # Separate the page into 2 columns (left: image, right: chat).
    # We'll do a simple Grid with 2 columns or 2 Div side by side. 
    # Pico CSS might style it nicely. For clarity, we just do some inline style.

    # LEFT COLUMN: Image
    left_col = Div(
        H2("Generated Image"),
        # If there's a stored image_url, show it
        (Img(src=sess["image_url"], style="max-width:100%;") if sess["image_url"] else 
         Div("💡 Try asking: 'Generate an image of a mountain landscape at sunset'")),
        style="flex:1; margin-right:1rem;"
    )

    # RIGHT COLUMN: Chat UI
    #  - Show existing chat messages
    #  - Show a form for new prompt
    chat_divs = []
    for msg in sess["messages"]:
        if msg["role"] == "user":
            chat_divs.append(
                Div(
                    B("You: "),
                    Div(msg["content"], cls="marked"),
                    cls="user-bubble"
                )
            )
        else:
            # "assistant"/"system"
            chat_divs.append(
                Div(
                    B("Assistant: "),
                    Div(msg["content"], cls="marked"),
                    cls="assistant-bubble"
                )
            )

    # A form to send a new "prompt" 
    chat_form = Form(
        Input(name="prompt", placeholder="What do you want to discuss or create?", required=True),
        Button("Send"),
        method="post"
    )

    right_col = Div(
        H2("Chat Interface"),
        *chat_divs,
        chat_form,
        style="flex:1;"
    )

    # Combine into a row
    row = Div(left_col, right_col, style="display:flex;")

    # A "Clear" button that links to /clear
    # (We'll style it as a small link or button.)
    clear_link = A("Clear Chat & Image", href="/clear", cls="secondary")

    # Return an entire page
    return Titled("AI Chat & Image Generator",
        # For Markdown rendering & code highlighting
        MarkdownJS(),
        HighlightJS(langs=["python","javascript","html","css"]),

        # Top-level content
        row,
        Div(clear_link, style="margin-top:1rem;")
    )


# 4) Route to clear the chat & image
@rt("/clear")
def get(sess):
    sess["messages"] = []
    sess["image_url"] = None
    return RedirectResponse("/", status_code=303)


serve()