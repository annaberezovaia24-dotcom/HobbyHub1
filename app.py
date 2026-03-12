import streamlit as st
from openai import OpenAI

# Page title
st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Talk with the bot about hobbies, interests, and fun activities!")

# Check API key
if "OPENAI_API_KEY" not in st.secrets:
    st.error("API key not found. Please add OPENAI_API_KEY to .streamlit/secrets.toml")
    st.stop()

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask about hobbies or interests...")

if prompt:
    
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # System prompt to guide chatbot
    system_prompt = """
    You are a friendly chatbot that helps people explore hobbies and interests.
    Suggest fun hobbies like:
    - Sports
    - Art
    - Music
    - Gaming
    - Reading
    - Outdoor activities
    - Technology hobbies
    Ask questions to learn about the user’s interests and suggest new hobbies.
    """

    # Create response
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
