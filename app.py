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
        "keywords": ["science", "experiment"],
        "responses": [
            "That's really interesting! Science is amazing 🔬",
            "Nice! Learning science is exciting 🧪"
        ],
        "suggestions": ["home experiments", "robotics", "coding"]
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

# Knowledge base
knowledge = {
    "coding": "Coding means writing instructions for a computer so it can do tasks 💻"
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

if "last_suggestion" not in st.session_state:
    st.session_state.last_suggestion = None

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

    # ✅ 2. NEGATIVE FEEDBACK (NEW 🔥)
    elif any(word in text for word in ["hate", "don't like", "do not like", "dislike"]):
        topic = st.session_state.last_topic

        if topic:
            # remove last suggestion
            if st.session_state.last_suggestion:
                st.session_state.used_suggestions.append(st.session_state.last_suggestion)

            # pick new suggestion
            available = [s for s in hobby_data[topic]["suggestions"]
                         if s not in st.session_state.used_suggestions]

            if not available:
                available = hobby_data[topic]["suggestions"]

            new_suggestion = random.choice(available)
            st.session_state.last_suggestion = new_suggestion

            response = (
                "No problem! 😊 Not everyone likes that.\n\n"
                f"💡 Maybe you could try **{new_suggestion}** instead!"
            )
        else:
            response = "Got it! 😊 What kinds of hobbies do you prefer?"

    # ✅ 3. "What is ..." question
    elif text.startswith("what is"):
        topic = text.replace("what is", "").strip()
        response = knowledge.get(topic, f"{topic.capitalize()} is something interesting to explore! 😊")

    # ✅ 4. Detect hobby
    for hobby, data in hobby_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                st.session_state.last_topic = hobby
                detected = True

                base = random.choice(data["responses"])

                available = [s for s in data["suggestions"]
                             if s not in st.session_state.used_suggestions]

                if not available:
                    available = data["suggestions"]

                suggestion = random.choice(available)

                st.session_state.used_suggestions.append(suggestion)
                st.session_state.last_suggestion = suggestion

                response = f"{base}\n\n💡 You could also try **{suggestion}**!"
                break
        if detected:
            break

    # ✅ 5. Follow-up
    if not response and st.session_state.last_topic:
        topic = st.session_state.last_topic
        suggestion = random.choice(hobby_data[topic]["suggestions"])
        response = f"That sounds great! 😊\n\n💡 You might also enjoy **{suggestion}**!"

    # ✅ 6. Fallback
    if not response:
        response = random.choice([
            "That sounds fun! 😊 Tell me more!",
            "Nice! What do you enjoy most about it?",
            "Cool! How did you get into that?"
        ])

    # 🚫 Avoid repeating
    if response == st.session_state.last_response:
        response += "\n\nTell me more! 😊"

    st.session_state.last_response = response

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
