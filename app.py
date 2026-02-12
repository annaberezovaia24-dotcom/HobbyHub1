import streamlit as st
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("💬 My Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Store user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from OpenAI
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
    )

    reply = response.choices[0].message.content

    # Store assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Display assistant reply
    with st.chat_message("assistant"):
        st.markdown(reply)
