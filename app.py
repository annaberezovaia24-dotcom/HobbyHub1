import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Tell me what you like, and I'll suggest similar hobbies!")

# Hobby categories
hobby_data = {
    "sports": {
        "keywords": ["tennis", "football", "basketball", "cycling", "padel"],
        "similar": ["badminton", "running", "swimming", "volleyball", "table tennis"],
        "response": "Nice! You seem to enjoy sports 💪"
    },
    "creative": {
        "keywords": ["draw", "drawing", "painting"],
        "similar": ["digital art", "animation", "sketching", "graphic design"],
        "response": "That's awesome! You're creative 🎨"
    },
    "science": {
        "keywords": ["science", "experiment", "physics", "chemistry"],
        "similar": ["robotics", "coding", "astronomy", "engineering projects"],
        "response": "Very interesting! You like learning 🔬"
    },
    "music": {
        "keywords": ["music", "guitar", "piano", "sing"],
        "similar": ["drums", "ukulele", "songwriting", "music production"],
        "response": "Nice! Music is a great hobby 🎵"
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

if "last_category" not in st.session_state:
    st.session_state.last_category = None

if "last_suggestions" not in st.session_state:
    st.session_state.last_suggestions = []

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
    detected = False

    # ✅ 1. Greetings
    if any(word in text for word in ["hi", "hello", "hey"]):
        response = random.choice(greetings)

    # ✅ 2. Dislike handling
    elif any(word in text for word in ["don't like", "do not like", "hate", "dislike"]):
        category = st.session_state.last_category

        if category:
            # mark previous suggestions as rejected
            st.session_state.rejected.extend(st.session_state.last_suggestions)

            # pick new ones
            available = [
                h for h in hobby_data[category]["similar"]
                if h not in st.session_state.rejected
            ]

            if not available:
                available = hobby_data[category]["similar"]

            new_suggestions = random.sample(available, min(3, len(available)))
            st.session_state.last_suggestions = new_suggestions

            response = (
                "No worries 😊 Not everyone likes that!\n\n"
                "💡 How about trying:\n"
            )

            for s in new_suggestions:
                response += f"- **{s}**\n"

            response += "\nDo any of these sound better?"
        else:
            response = "No problem 😊 What kind of hobbies do you prefer?"

    # ✅ 3. Detect hobby and suggest similar ones
    else:
        for category, data in hobby_data.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    detected = True
                    st.session_state.last_category = category

                    # avoid repeats
                    available = [
                        h for h in data["similar"]
                        if h not in st.session_state.rejected
                    ]

                    if not available:
                        available = data["similar"]

                    suggestions = random.sample(available, min(3, len(available)))
                    st.session_state.last_suggestions = suggestions

                    response = (
                        f"{data['response']} 😊\n\n"
                        "💡 You might also enjoy:\n"
                    )

                    for s in suggestions:
                        response += f"- **{s}**\n"

                    response += "\nWhich one sounds interesting?"

                    break
            if detected:
                break

    # ✅ 4. Fallback
    if not response:
        response = random.choice([
            "That sounds interesting! 😊 Tell me more!",
            "Nice! What kind of hobbies do you enjoy?",
            "Cool! Tell me more about that!"
        ])

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
