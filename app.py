import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat and discover hobbies you'll enjoy!")

# Hobby system
hobby_data = {
    "drawing": {
        "keywords": ["draw", "drawing"],
        "responses": [
            "Nice! Art is a great way to express yourself ✏️",
            "That’s awesome! Drawing is very creative 🎨"
        ],
        "suggestions": ["digital art", "painting", "animation"]
    }
}

# Greeting responses
greetings = [
    "Hi there! 😊 What hobbies do you enjoy?",
    "Hello! 👋 Tell me about your hobbies!",
    "Hey! 😄 What do you like to do in your free time?"
]

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_response" not in st.session_state:
    st.session_state.last_response = ""

# Show chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input
user_input = st.chat_input("Tell me about your hobbies...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    text = user_input.lower()
    response = ""
    detected = False

    # ✅ 1. Greeting detection (FIRST!)
    if any(word in text for word in ["hi", "hello", "hey"]):
        response = random.choice(greetings)

    # ✅ 2. Hobby detection
    if not response:
        for hobby, data in hobby_data.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    detected = True

                    base = random.choice(data["responses"])
                    suggestion = random.choice(data["suggestions"])

                    response = f"{base} 😊\n\n💡 You could also try **{suggestion}**!"
                    break
            if detected:
                break

    # ✅ 3. Fallback
    if not response:
        response = random.choice([
            "That sounds interesting! 😊 Tell me more!",
            "Nice! What else do you enjoy?",
            "Cool! Can you tell me more about that?"
        ])

    # 🚫 Prevent repeating same response
    if response == st.session_state.last_response:
        response += "\n\nTell me more! 😊"

    st.session_state.last_response = response

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
