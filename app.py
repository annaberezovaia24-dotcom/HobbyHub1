import streamlit as st

st.title("🤖 HobbyHub Chatbot (No API Version)")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Simple chatbot logic
def chatbot_response(user_input):
    user_input = user_input.lower()

    if "hello" in user_input:
        return "Hi there! 👋 Welcome to HobbyHub!"
    elif "hobby" in user_input:
        return "We have art, music, coding, sports and more! 🎨🎵💻⚽"
    elif "help" in user_input:
        return "Sure! Tell me what hobby you're interested in."
    elif "bye" in user_input:
        return "Goodbye! Come back soon 😊"
    else:
        return "That's interesting! Tell me more!"

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    response = chatbot_response(prompt)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistant"):
        st.write(response)
