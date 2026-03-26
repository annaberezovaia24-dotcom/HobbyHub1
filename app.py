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
            "Nice! Science is exciting 🧪"
        ],
        "suggestions": ["robotics", "coding", "home experiments"]
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

if "last_suggestion" not in st.session_state:
    st.session_state.last_suggestion = None

if "rejected" not in st.session_state:
    st.session_state.rejected = []

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

    # ✅ 1. Greeting
    if any(word in text for word in ["hi", "hello", "hey"]):
        response = random.choice(greetings)

    # ✅ 2. NEGATIVE FEEDBACK (FIXED 🔥)
    elif any(word in text for word in ["don't like", "do not like", "hate", "dislike"]):

        topic = st.session_state.last_topic

        if topic:
            # remember rejected suggestion
            if st.session_state.last_suggestion:
                st.session_state.rejected.append(st.session_state.last_suggestion)

            # choose NEW suggestion (not rejected)
            available = [
                s for s in hobby_data[topic]["suggestions"]
                if s not in st.session_state.rejected
            ]

            # if all rejected → reset
            if not available:
                st.session_state.rejected = []
                available = hobby_data[topic]["suggestions"]

            new_suggestion = random.choice(available)
            st.session_state.last_suggestion = new_suggestion

            response = (
                "No worries! 😊 Not everyone likes that.\n\n"
                f"💡 How about trying **{new_suggestion}** instead?"
            )

        else:
            response = "Got it! 😊 Tell me what you enjoy!"

    # ✅ 3. Detect hobby
    else:
        for hobby, data in hobby_data.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    st.session_state.last_topic = hobby

                    base = random.choice(data["responses"])
                    suggestion = random.choice(data["suggestions"])

                    st.session_state.last_suggestion = suggestion
                    st.session_state.rejected = []  # reset rejects for new topic

                    response = f"{base}\n\n💡 You could also try **{suggestion}**!"
                    break
            if response:
                break

    # ✅ 4. Fallback (only if nothing else matched)
    if not response:
        response = random.choice([
            "That sounds fun! 😊 Tell me more!",
            "Nice! What do you enjoy most about it?",
            "Cool! How did you get into that?"
        ])

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
