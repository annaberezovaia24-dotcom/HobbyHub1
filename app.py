import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Tell me what you like, and I'll suggest similar hobbies!")

# Hobby categories
hobby_data = {
    "sports": {
        "keywords": ["tennis", "football", "basketball", "cycling", "padel"],
        "similar": ["badminton", "running", "swimming", "table tennis", "volleyball"],
        "response": "Nice! You seem to enjoy sports 💪"
    },

    "creative": {
        "keywords": ["draw", "drawing", "painting"],
        "similar": ["digital art", "sketching", "animation", "graphic design"],
        "response": "That's awesome! You're creative 🎨"
    },

    "science": {
        "keywords": ["science", "experiment", "physics", "chemistry"],
        "similar": ["robotics", "coding", "astronomy", "engineering projects"],
        "response": "Very interesting! You like learning 🔬"
    },

    "music": {
        "keywords": ["music", "guitar", "piano", "sing"],
        "similar": ["drums", "ukulele", "music production", "songwriting"],
        "response": "Nice! Music is a great hobby 🎵"
    }
}

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    # Detect hobby category
    for category, data in hobby_data.items():
        for keyword in data["keywords"]:
            if keyword in text:
                detected = True

                # Avoid repeating suggestions
                available = [
                    h for h in data["similar"]
                    if h not in st.session_state.used_suggestions
                ]

                if not available:
                    available = data["similar"]

                # Pick 2-3 similar hobbies
                suggestions = random.sample(available, min(3, len(available)))

                # Save used
                st.session_state.used_suggestions.extend(suggestions)

                response = (
                    f"{data['response']} 😊\n\n"
                    f"💡 You might also enjoy:\n"
                )

                for s in suggestions:
                    response += f"- **{s}**\n"

                response += "\nWhich one sounds interesting to you?"

                break
        if detected:
            break

    # If nothing detected
    if not response:
        response = random.choice([
            "That sounds interesting! 😊 Can you tell me more?",
            "Nice! What kind of hobbies do you enjoy?",
            "Cool! Tell me more about what you like!"
        ])

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
