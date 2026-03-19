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
            "That's awesome! Drawing is very creative 🎨",
            "Nice! Art is a great way to express yourself ✏️"
        ],
        "suggestions": ["digital art", "painting", "animation"]
    },
    "sports": {
        "keywords": ["tennis", "football", "basketball"],
        "responses": [
            "Nice! Staying active is great 💪",
            "That's awesome! Sports are really fun!"
        ],
        "suggestions": ["running", "badminton", "cycling"]
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

if "last_suggestion" not in st.session_state:
    st.session_state.last_suggestion = None

if "used_suggestions" not in st.session_state:
    st.session_state.used_suggestions = []

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

    # ✅ 1. Greeting
    if any(word in text for word in ["hi", "hello", "hey"]):
        response = random.choice(greetings)

    # ✅ 2. User ACCEPTS suggestion
    elif st.session_state.last_suggestion and st.session_state.last_suggestion in text:
        suggestion = st.session_state.last_suggestion
        response = f"Great choice! 😊 {suggestion.capitalize()} is really fun!\n\n"

        # Continue conversation
        response += random.choice([
            "What made you interested in it?",
            "Have you tried it before?",
            "Do you want to learn it or just explore it?"
        ])

        st.session_state.last_suggestion = None

    # ✅ 3. Detect hobbies
    else:
        for hobby, data in hobby_data.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    detected = True

                    base = random.choice(data["responses"])

                    # pick NEW suggestion (not used before)
                    available = [s for s in data["suggestions"] if s not in st.session_state.used_suggestions]

                    if not available:
                        available = data["suggestions"]

                    suggestion = random.choice(available)

                    st.session_state.used_suggestions.append(suggestion)
                    st.session_state.last_suggestion = suggestion

                    response = (
                        f"{base} 😊\n\n"
                        f"💡 You could also try **{suggestion}**!\n\n"
                        f"What do you think?"
                    )
                    break
            if detected:
                break

    # ✅ 4. If user asks for ideas
    if not response and ("suggest" in text or "idea" in text):
        all_suggestions = []
        for h in hobby_data.values():
            all_suggestions.extend(h["suggestions"])

        available = [s for s in all_suggestions if s not in st.session_state.used_suggestions]

        if not available:
            available = all_suggestions

        suggestion = random.choice(available)

        st.session_state.used_suggestions.append(suggestion)
        st.session_state.last_suggestion = suggestion

        response = f"You could try **{suggestion}**! 😊 What do you think?"

    # ✅ 5. Smart fallback
    if not response:
        response = random.choice([
            "That sounds interesting! 😊 What do you enjoy most about it?",
            "Nice! How did you get into that?",
            "Cool! What do you like most about it?"
        ])

    # 🚫 Prevent repeating
    if response == st.session_state.last_response:
        response += "\n\nTell me more! 😊"

    st.session_state.last_response = response

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
