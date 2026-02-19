import streamlit as st
import os

# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------
st.set_page_config(
    page_title="HobbyHub Chatbot",
    page_icon="🎨",
    layout="centered"
)

# --------------------------------------------------
# DISPLAY LOGO
# --------------------------------------------------
if os.path.exists("Logo.png"):
    st.image("Logo.png", width=180)

st.title("🎨 HobbyHub Chatbot")
st.caption("Ask me about hobbies, art, music, coding, sports and more!")

# --------------------------------------------------
# LOAD DOCUMENTS FROM FOLDER
# --------------------------------------------------
def load_documents():
    knowledge = ""

    if os.path.exists("Documents"):
        for file in os.listdir("Documents"):
            file_path = os.path.join("Documents", file)

            if file.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    knowledge += f.read() + "\n"

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
    if user_input in knowledge_base and len(user_input) > 3:
        return "📄 I found information about that in our HobbyHub documents!"

    elif "hello" in user_input or "hi" in user_input:
        return "Hi there! 👋 Welcome to HobbyHub!"

    elif "hobby" in user_input:
        return "We have art 🎨, music 🎵, coding 💻, sports ⚽ and more!"

    elif "art" in user_input:
        return "Art is a creative hobby! You can try painting, drawing or digital art."

    elif "music" in user_input:
        return "Music is amazing! You can learn instruments, singing, or music production."

    elif "coding" in user_input:
        return "Coding is a powerful hobby! You can build apps, websites and games."

    elif "sports" in user_input:
        return "Sports keep you healthy! Football, basketball, swimming and more!"

    elif "help" in user_input:
        return "Sure! Tell me what hobby you're interested in."

    elif "bye" in user_input:
        return "Goodbye! Come back soon 😊"

    else:
        return "That sounds interesting! Tell me more about it!"

# --------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --------------------------------------------------
# USER INPUT BOX
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

    # Generate response
    response = chatbot_response(prompt)

    # Add assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)
