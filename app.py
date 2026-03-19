import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat and discover hobbies you'll enjoy!")

# Hobby system
hobby_data = {
    "swimming": {
        "keywords": ["swim", "swimming"],
        "responses": [
            "Swimming is awesome 🌊",
            "Nice! Swimming is great exercise 💪"
        ],
        "suggestions": ["diving", "water polo", "surfing"]
    },
    "music": {
        "keywords": ["guitar", "music", "sing"],
        "responses": [
            "That's cool! Music is a great hobby 🎵",
            "Nice! Playing music is really fun 🎸"
        ],
        "suggestions": ["learning piano", "writing songs", "music production"]
    },
    "drawing": {
        "keywords": ["draw", "drawing"],
        "responses": [
            "Drawing is very creative 🎨",
            "Nice! Art is a great way to express yourself ✏️"
        ],
        "suggestions": ["digital art", "painting", "animation"]
    }
}

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

    # Detect hobbies
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

    # If nothing detected → use varied fallback
    if not detected:
        fallback_options = [
            "That sounds fun! 😊 What do you enjoy most about it?",
            "Nice! Tell me more about that!",
            "Cool! What got you interested in that hobby?"
        ]
        response = random.choice(fallback_options)

    # 🚫 Prevent repeating same response
    if response == st.session_state.last_response:
        response += "\n\nTell me more! 😊"

    st.session_state.last_response = response

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
