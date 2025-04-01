import streamlit as st
from openai import OpenAI
import time
from PIL import Image
import requests
from io import BytesIO
import os
import dotenv
dotenv.load_dotenv()

client = OpenAI(
  organization=os.environ.get('ORG_ID'),
  project=os.environ.get('PROJECT_ID')
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_image" not in st.session_state:
    st.session_state.current_image = None

# Page configuration
st.set_page_config(layout="wide")

# Title
st.title("AI Chat & Image Generator")

# Create two columns
col1, col2 = st.columns(2)

# Image display column
with col1:
    st.header("Generated Image")
    if st.session_state.current_image:
        st.image(st.session_state.current_image)
    else:
        st.info("💡 Try asking: 'Generate an image of a mountain landscape at sunset'")

# Function to generate image
def generate_image(prompt):
    try:
        with st.spinner("🎨 Generating image with DALL-E 3..."):
            # Create a more detailed prompt for better results
            enhanced_prompt = f"High quality, detailed image of: {prompt}"
            
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            # Get the image URL
            image_url = image_response.data[0].url
            
            # Download and process the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image = Image.open(BytesIO(image_response.content))
                return image
            else:
                st.error(f"Failed to download image: Status code {image_response.status_code}")
                return None
    except Exception as e:
        st.error(f"Error generating image: {str(e)}")
        return None

# Chat interface column
with col2:
    st.header("Chat Interface")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to discuss or create?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        print('HELLO!')
        # Display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Generate chat response
            try:
                chat_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": m["role"], "content": m["content"]} 
                             for m in st.session_state.messages],
                    max_tokens=150
                )
                response_text = chat_response.choices[0].message.content
                message_placeholder.write(response_text)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text})
                
                generated_image = generate_image(prompt)
                if generated_image:
                    st.session_state.current_image = generated_image
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Error in chat completion: {str(e)}")

# Add a clear chat button
if st.sidebar.button("Clear Chat & Image"):
    st.session_state.messages = []
    st.session_state.current_image = None
    st.rerun()

# Add API key input in sidebar
with st.sidebar:
    st.header("Settings")
    new_api_key = st.text_input("OpenAI API Key (optional)", type="password")
    if new_api_key:
        st.session_state["OPENAI_API_KEY"] = new_api_key
        client = OpenAI(api_key=new_api_key)