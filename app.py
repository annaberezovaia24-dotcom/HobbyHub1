import streamlit as st
import os
from openai import OpenAI

# Page settings
st.set_page_config(page_title="Hobby & Interests Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Talk with the bot about hobbies, interests, and fun activities!")

# Get API key safely
api_key = os.getenv("OPENAI_API_KEY")

# If API key missing, show input box instead of crashing
if not api_key:
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if not api_key:
    st.warning("Please enter your OpenAI API key to continue.")
    st.stop()

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """You are a friendly chatbot that helps users explore hobbies and interests.
            Suggest activities like sports, art, music, reading, gaming, outdoor activities,
            creative hobbies, and technology hobbies. Ask questions to learn about the user."""
        }
    ]

# Display previous messages
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Ask about hobbies or interests...")

if prompt:
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
