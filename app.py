import streamlit as st
import os
from openai import OpenAI

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="HobbyHub Chatbot",
    page_icon="🎨",
    layout="centered"
)

# --------------------------------------------------
# OPENAI API
# --------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --------------------------------------------------
# LOGO
# --------------------------------------------------
logo_path = "Logo.png"

if os.path.exists(logo_path) and os.path.isfile(logo_path):
    st.image(logo_path, width=180)

st.title("🎨 HobbyHub Chatbot")
st.caption("Ask me about hobbies like art, music, coding, sports and more!")

# --------------------------------------------------
# LOAD DOCUMENTS SAFELY
# --------------------------------------------------
def load_documents():

    knowledge = ""
    folder = "Documents"

    if os.path.exists(folder) and os.path.isdir(folder):

        for file in os.listdir(folder):

            file_path = os.path.join(folder, file)

            if file.endswith(".txt") and os.path.isfile(file_path):

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        knowledge += f.read() + "\n"

                except:
                    pass

    return knowledge


knowledge_base = load_documents()

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! 👋 Welcome to HobbyHub. Tell me about your hobbies!"
        }
    ]

# --------------------------------------------------
# DISPLAY CHAT
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
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    # --------------------------------------------------
    # SYSTEM PROMPT
    # --------------------------------------------------
    system_prompt = f"""
You are HobbyHub, a friendly chatbot that talks about hobbies.

Rules:
- Have natural conversations
- Suggest hobbies
- Ask follow-up questions
- Encourage creativity
- Use the knowledge base if helpful

Knowledge Base:
{knowledge_base}
"""

    # --------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content

    # Save response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)
