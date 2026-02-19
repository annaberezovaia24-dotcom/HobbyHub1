import streamlit as st
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="HobbyHub Chatbot",
    page_icon="🎨",
    layout="centered"
)

# --------------------------------------------------
# SAFE LOGO DISPLAY
# --------------------------------------------------
logo_path = "Logo.png"

if os.path.exists(logo_path) and os.path.isfile(logo_path):
    st.image(logo_path, width=180)

st.title("🎨 HobbyHub Chatbot")
st.caption("Ask me about art, music, coding, sports and more!")

# --------------------------------------------------
# LOAD DOCUMENTS SAFELY
# --------------------------------------------------
def load_documents():
    knowledge = ""
    folder_path = "Documents"

    # Only read if folder exists AND is a directory
    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            # Only read .txt files
            if file.endswith(".txt") and os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        knowledge += f.read() + "\n"
                except Exception:
                    pass

    return knowledge.lower()

knowledge_base = load_documents()

# --------------------------------------------------
# INITIALIZE CHAT HISTORY
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# CHATBOT LOGIC
# --------------------------------------------------
def chatbot_response(user_input):
    user_input = user_input.lower()

    # Search inside documents
    if knowledge_base and any(word in knowledge_base for word in user_input.split()):
        return "📄 I found something related to that in our HobbyHub documents!"

    # Predefined responses
    elif "hello" in user_input or "hi" in user_input:
        return "Hi there! 👋 Welcome to HobbyHub!"

    elif "art" in user_input:
        return "🎨 Art is a creative hobby! Try painting, drawing, or digital art."

    elif "music" in user_input:
        return "🎵 Music is amazing! You can learn instruments or music production."

    elif "coding" in user_input:
        return "💻 Coding lets you build apps, websites, and games!"

    elif "sports" in user_input:
        return "⚽ Sports keep you active! Football, basketball, swimming and more!"

    elif "help" in user_input:
        return "Sure! Tell me which hobby you're interested in."

    elif "bye" in user_input:
        return "Goodbye! Come back soon 😊"

    else:
        return "That sounds interesting! Tell me more!"

# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --------------------------------------------------
# USER INPUT
# --------------------------------------------------
prompt = st.chat_input("Type your message here...")

if prompt:
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Generate bot response
    response = chatbot_response(prompt)

    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)
