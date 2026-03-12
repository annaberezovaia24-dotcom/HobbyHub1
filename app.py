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
# OPENAI CLIENT
# --------------------------------------------------
client = OpenAI(api_key="YOUR_API_KEY_HERE")

# --------------------------------------------------
# LOGO
# --------------------------------------------------
logo_path = "Logo.png"

if os.path.exists(logo_path):
    st.image(logo_path, width=180)

st.title("🎨 HobbyHub Chatbot")
st.caption("Ask me about hobbies like art, music, coding, sports and more!")

# --------------------------------------------------
# LOAD DOCUMENTS
# --------------------------------------------------
def load_documents():

    knowledge = ""
    folder = "Documents"

    if os.path.exists(folder):

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            if file.endswith(".txt"):
                with open(path, "r", encoding="utf-8") as f:
                    knowledge += f.read() + "\n"

    return knowledge


knowledge_base = load_documents()

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! 👋 Welcome to HobbyHub. Tell me what hobbies you enjoy!"
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
    # AI RESPONSE
    # --------------------------------------------------

    system_prompt = f"""
You are HobbyHub, a friendly chatbot that talks with users about hobbies.

Your goals:
- Have natural conversations
- Ask follow-up questions
- Suggest hobbies
- Encourage creativity
- Use the knowledge base if helpful

Knowledge Base:
{knowledge_base}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            *st.session_state.messages
        ]
    )

    reply = response.choices[0].message.content

    # Add assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )

    with st.chat_message("assistant"):
        st.write(reply)
