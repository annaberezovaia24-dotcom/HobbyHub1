import streamlit as st
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="HobbyHub Chatbot", page_icon="🎨")

# ----------------------------
# LOAD LOGO
# ----------------------------
if os.path.exists("Logo.png"):
    st.image("Logo.png", width=200)

st.title("🎨 HobbyHub Chatbot")

# ----------------------------
# LOAD DOCUMENTS
# ----------------------------
def load_documents():
    documents_text = ""

    if os.path.exists("Documents"):
        for file in os.listdir("Documents"):
            file_path = os.path.join("Documents", file)

            if file.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    documents_text += f.read() + "\n"

    return documents_text.lower()

knowledge_base = load_documents()

# ----------------------------
# INITIALIZE CHAT HISTORY
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# SIMPLE DOCUMENT SEARCH BOT
# ----------------------------
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Search in knowledge base
    if user_input in knowledge_base:
        return "📄 I found something about that in our documents!"

    elif "hello" in user_input:
        return "Hi there! 👋 Welcome to HobbyHub!"

    elif "hobby" in user_input:
        return "We have art, music, coding, sports and more! 🎨🎵⚽💻"

    elif "help" in user_input:
        return "Sure! Tell me what hobby you're interested in."

    elif "bye" in user_input:
        return "Goodbye! Come back soon 😊"

    else:
        return "That's interesting! Tell me more!"

# ----------------------------
# DISPLAY CHAT HISTORY
# ----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]()_
