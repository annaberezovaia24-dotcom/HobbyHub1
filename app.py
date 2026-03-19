import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat and discover hobbies you'll enjoy!")

# Hobby system (EXPANDED)
hobby_data = {
    "sports": {
        "keywords": ["cycling", "bike", "tennis", "football", "basketball"],
        "responses": [
            "That's awesome! Staying active is great 🚴",
            "Nice! Sports are really fun and healthy 💪"
        ],
        "suggestions": ["running", "swimming", "hiking"]
    },

    "science": {
        "keywords": ["science", "experiment", "chemistry", "physics"],
        "responses": [
            "That's really interesting! Science is amazing 🔬",
            "Nice! Learning science can be really exciting 🧪"
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

    # ✅ 2. Detect hobby/topic
    for hobby, data in hobby_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                st.session_state.last_topic = hobby
                detected = True

                base = random.choice(data["responses"])
                suggestion = random.choice(data["suggestions"])

                response = f"{base}\n\n💡 You could also try **{suggestion}**!"
                break
        if detected:
            break

    # ✅ 3. Handle follow-up sentences (IMPORTANT FIX)
    if not response and st.session_state.last_topic:

        topic = st.session_state.last_topic

        # Specific logic for science
        if topic == "science" and ("experiment" in text or "make" in text):
            response = random.choice([
                "That's awesome! Doing experiments is the best part of science 🧪",
                "Nice! Experiments make science really fun and hands-on 🔬"
            ]) + "\n\n💡 You could try some simple home experiments!"

        # Specific logic for sports
        elif topic == "sports":
            response = random.choice([
                "Nice! Staying active is great for your health 💪",
                "That sounds fun! Do you do it often?"
            ]) + "\n\n💡 You could also try hiking or swimming!"

        # General topic follow-up
        else:
            suggestion = random.choice(hobby_data[topic]["suggestions"])
            response = f"That’s really interesting! 😊\n\n💡 You might also enjoy **{suggestion}**!"

    # ✅ 4. Questions
    if not response and ("what" in text or "how" in text or "which" in text):
        if st.session_state.last_topic:
            topic = st.session_state.last_topic
            suggestion = random.choice(hobby_data[topic]["suggestions"])
            response = f"Good question! 😊 You could try **{suggestion}**."
        else:
            response = "Good question! 😊 What hobbies are you interested in?"

    # ✅ 5. Fallback (LESS GENERIC NOW)
    if not response:
        response = random.choice([
            "That sounds fun! 😊 What do you like most about it?",
            "Nice! How did you get into that?",
            "Cool! What part do you enjoy the most?"
        ])

    # 🚫 Prevent repeating
    if response == st.session_state.last_response:
        response += "\n\nTell me more! 😊"

    st.session_state.last_response = response

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    
