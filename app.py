import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat about your hobbies and discover new ones!")

# Hobby detection with better keywords
hobby_data = {
    "drawing": {
        "keywords": ["draw", "drawing", "sketch"],
        "responses": [
            "That’s awesome! Drawing is a great creative hobby 🎨",
            "Nice! Drawing helps you express your imagination ✏️"
        ],
        "followups": [
            "Do you like drawing people or characters?",
            "What do you enjoy drawing the most?",
            "Do you draw digitally or on paper?"
        ],
        "suggestions": [
            "You could try digital art or animation!",
            "Maybe explore character design or comics!",
            "You might enjoy painting or graphic design too!"
        ]
    },

    "sports": {
        "keywords": ["tennis", "football", "basketball", "swim", "swimming"],
        "responses": [
            "That’s great! Sports are really good for you 💪",
            "Nice! Staying active is always a good thing!"
        ],
        "followups": [
            "Do you play just for fun or competitively?",
            "How often do you practice?",
        ],
        "suggestions": [
            "You could try other sports like badminton or running!",
            "Maybe join a local team or club!"
        ]
    }
}

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_hobbies" not in st.session_state:
    st.session_state.user_hobbies = []

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
                st.session_state.user_hobbies.append(hobby)

                # Build smart response
                response = (
                    random.choice(data["responses"]) + " " +
                    random.choice(data["followups"]) + "\n\n" +
                    "💡 Suggestion: " + random.choice(data["suggestions"])
                )
                break
        if detected:
            break

    # If user asks for suggestions
    if not detected and ("suggest" in text or "idea" in text):
        if st.session_state.user_hobbies:
            hobby = random.choice(st.session_state.user_hobbies)
            response = f"Since you like {hobby}, here’s an idea: " + \
                       random.choice(hobby_data[hobby]["suggestions"])
        else:
            response = "You could try drawing, sports, music, or gaming! What sounds interesting?"

    # Greeting
    elif not detected and ("hello" in text or "hi" in text):
        response = "Hi! 😊 Tell me what hobbies you enjoy!"

    # Fallback (IMPORTANT FIX)
    elif not detected:
        response = "That sounds really interesting! 😊 Can you tell me more about what you like specifically?"

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
