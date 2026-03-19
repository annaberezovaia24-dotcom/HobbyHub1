import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat and discover hobbies you'll enjoy!")

# Hobby system
hobby_data = {
    "music": {
        "keywords": ["music", "guitar", "piano", "sing"],
        "responses": [
            "That's awesome! Music is a great hobby 🎵",
            "Nice! Playing music is really fun 🎸"
        ],
        "suggestions": ["guitar", "piano", "drums", "ukulele"],
        "questions": {
            "instrument": [
                "You could try **guitar** — it's very popular and beginner-friendly 🎸",
                "Piano is a great choice if you like melodies 🎹",
                "Drums are fun if you enjoy rhythm 🥁"
            ]
        }
    },

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
        "suggestions": ["running", "cycling", "swimming"]
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

    # ✅ 2. Detect topic (hobby)
    for hobby, data in hobby_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                st.session_state.last_topic = hobby
                detected = True

                response = random.choice(data["responses"])
                break
        if detected:
            break

    # ✅ 3. Answer QUESTIONS
    if "what" in text or "which" in text or "how" in text:

        topic = st.session_state.last_topic

        # If asking about music instruments
        if topic == "music" and "instrument" in text:
            response = random.choice(hobby_data["music"]["questions"]["instrument"])

        elif topic:
            # general answer
            suggestion = random.choice(hobby_data[topic]["suggestions"])
            response = f"Good question! 😊 You could try **{suggestion}**. It’s a great option!"

        else:
            response = "Good question! 😊 Can you tell me what hobbies you're interested in?"

    # ✅ 4. Suggest ideas
    if not response and ("suggest" in text or "idea" in text):
        topic = st.session_state.last_topic

        if topic:
            suggestion = random.choice(hobby_data[topic]["suggestions"])
            response = f"You could try **{suggestion}**! What do you think?"
        else:
            response = "You could try drawing, music, or sports! What sounds fun?"

    # ✅ 5. If hobby detected (normal reply + suggestion)
    if not response and detected:
        topic = st.session_state.last_topic
        suggestion = random.choice(hobby_data[topic]["suggestions"])

        response = f"{random.choice(hobby_data[topic]['responses'])}\n\n💡 You could also try **{suggestion}**!"

    # ✅ 6. Fallback
    if not response:
        response = random.choice([
            "That sounds interesting! 😊 Tell me more!",
            "Nice! What do you enjoy most about it?",
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
