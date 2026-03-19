import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat and discover hobbies you'll enjoy!")

# Hobby system
hobby_data = {
    "sports": {
        "keywords": ["tennis", "football", "basketball", "cycling", "padel"],
        "responses": [
            "That's awesome! Sports are really fun 💪",
            "Nice! Staying active is great 🚴"
        ],
        "suggestions": ["running", "swimming", "badminton", "hiking"]
    },

    "science": {
        "keywords": ["science", "experiment", "chemistry", "physics"],
        "responses": [
            "That's really interesting! Science is amazing 🔬",
            "Nice! Learning science can be exciting 🧪"
        ],
        "suggestions": ["home experiments", "robotics", "coding"]
    },

    "music": {
        "keywords": ["music", "guitar", "piano"],
        "responses": [
            "That's awesome! Music is a great hobby 🎵",
            "Nice! Playing music is really fun 🎸"
        ],
        "suggestions": ["guitar", "piano", "drums"]
    },

    "drawing": {
        "keywords": ["draw", "drawing"],
        "responses": [
            "That's awesome! Drawing is very creative 🎨",
            "Nice! Art is a great way to express yourself ✏️"
        ],
        "suggestions": ["digital art", "painting", "animation"]
    }
}

# Simple knowledge base (NEW ✨)
knowledge = {
    "coding": "Coding means writing instructions for a computer so it can do tasks. It’s used to build apps, games, and websites 💻",
    "robotics": "Robotics is about building and programming robots 🤖",
    "physics": "Physics is the study of how things move and work in the universe 🌍"
}

# Greetings
greetings = [
    "Hi there! 😊 What hobbies do you enjoy?",
    "Hello! 👋 Tell me about your hobbies!",
    "Hey! 😄 What do you like to do in your free time?"
]

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_topic" not in st.session_state:
    st.session_state.last_topic = None

if "used_suggestions" not in st.session_state:
    st.session_state.used_suggestions = []

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

    # ✅ 1. Greeting
    if any(word in text for word in ["hi", "hello", "hey"]):
        response = random.choice(greetings)

    # ✅ 2. "What is ..." questions (NEW FIX)
    elif text.startswith("what is"):
        topic = text.replace("what is", "").strip()

        if topic in knowledge:
            response = knowledge[topic]
        else:
            response = f"{topic.capitalize()} is something interesting! 😊 You can explore it as a hobby!"

    # ✅ 3. Detect hobby
    for hobby, data in hobby_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                st.session_state.last_topic = hobby
                detected = True

                base = random.choice(data["responses"])

                # Avoid repeating suggestions
                available = [s for s in data["suggestions"] if s not in st.session_state.used_suggestions]
                if not available:
                    available = data["suggestions"]

                suggestion = random.choice(available)
                st.session_state.used_suggestions.append(suggestion)

                response = f"{base}\n\n💡 You could also try **{suggestion}**!"
                break
        if detected:
            break

    # ✅ 4. Follow-up logic
    if not response and st.session_state.last_topic:
        topic = st.session_state.last_topic

        suggestion = random.choice(hobby_data[topic]["suggestions"])
        response = f"That sounds great! 😊\n\n💡 You might also enjoy **{suggestion}**!"

    # ✅ 5. Questions
    if not response and ("what" in text or "how" in text or "which" in text):
        if st.session_state.last_topic:
            topic = st.session_state.last_topic
            suggestion = random.choice(hobby_data[topic]["suggestions"])
            response = f"Good question! 😊 You could try **{suggestion}**!"
        else:
            response = "Good question! 😊 What hobbies are you interested in?"

    # ✅ 6. Fallback
    if not response:
        response = random.choice([
            "That sounds fun! 😊 What do you enjoy most about it?",
            "Nice! How did you get into that?",
            "Cool! Tell me more about that!"
        ])

    # 🚫 Avoid repeating
    if response == st.session_state.last_response:
        response += "\n\nTell me more! 😊"

    st.session_state.last_response = response

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
