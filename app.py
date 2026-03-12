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

if os.path.exists(logo_path):
    st.image(logo_path, width=180)

st.title("🎨 HobbyHub Chatbot")
st.caption("Ask me about art, music, coding, sports and more!")

# --------------------------------------------------
# LOAD DOCUMENTS
# --------------------------------------------------
def load_documents():
    knowledge = ""
    folder_path = "Documents"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):

        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)

            if file.endswith(".txt") and os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        knowledge += f.read() + "\n"
                except:
                    pass

    return knowledge.lower()

knowledge_base = load_documents()

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! 👋 Welcome to HobbyHub! Ask me about hobbies!"}
    ]

# --------------------------------------------------
# CHATBOT LOGIC
# --------------------------------------------------
def chatbot_response(user_input):

    user_input = user_input.lower()

    # Keyword groups
    art_words = ["art", "painting", "drawing", "sketch", "design"]
    music_words = ["music", "guitar", "piano", "sing", "instrument"]
    coding_words = ["coding", "programming", "python", "software", "developer"]
    sports_words = ["sports", "football", "basketball", "tennis", "swimming"]

    # Suggest hobbies
    if "hobby" in user_input or "suggest" in user_input:
        return """
Here are some hobbies you can try:

🎨 **Art** – drawing, painting, digital art  
🎵 **Music** – guitar, piano, singing  
💻 **Coding** – build websites, apps, or games  
⚽ **Sports** – football, basketball, swimming  
📚 **Reading** – explore new ideas and stories  
📸 **Photography** – capture creative photos
"""

    # Art
    elif any(word in user_input for word in art_words):
        return "🎨 Art is a creative hobby! Try painting, sketching, or digital illustration."

    # Music
    elif any(word in user_input for word in music_words):
        return "🎵 Music is a fun hobby! You could learn guitar, piano, or even music production."

    # Coding
    elif any(word in user_input for word in coding_words):
        return "💻 Coding is a powerful skill! You can build apps, websites, and even games."

    # Sports
    elif any(word in user_input for word in sports_words):
        return "⚽ Sports keep you healthy and active! Try football, basketball, swimming or cycling."

    # Greeting
    elif "hello" in user_input or "hi" in user_input:
        return "Hello! 👋 What hobbies are you interested in?"

    # Goodbye
    elif "bye" in user_input:
        return "Goodbye! 👋 Come back anytime to explore new hobbies."

    # Document search
    elif knowledge_base:
        for word in user_input.split():
            if word in knowledge_base:
                return "📄 I found something related to that in our HobbyHub documents!"

    # Default
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

    # Store user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.write(prompt)

    # Generate response
    response = chatbot_response(prompt)

    # Store assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    with st.chat_message("assistant"):
        st.write(response)
