import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat and discover hobbies you'll enjoy!")

# Hobby system
hobby_data = {
    "drawing": {
        "keywords": ["draw", "drawing", "sketch"],
        "suggestions": ["digital art", "animation", "painting", "character design"],
    },
    "sports": {
        "keywords": ["tennis", "football", "basketball"],
        "suggestions": ["running", "badminton", "cycling", "swimming"],
    }
}

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_hobbies" not in st.session_state:
    st.session_state.user_hobbies = []

if "last_suggestion" not in st.session_state:
    st.session_state.last_suggestion = None

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

    # 🔹 1. If user follows a suggestion
    if st.session_state.last_suggestion:
        if st.session_state.last_suggestion in text:
            response = f"Great choice! 😊 {st.session_state.last_suggestion.capitalize()} is really fun!\n\n"

            # Continue conversation based on suggestion
            if st.session_state.last_suggestion == "running":
                response += random.choice([
                    "Do you prefer running outdoors or on a treadmill?",
                    "Running is great for fitness! Do you run often?"
                ])
            elif st.session_state.last_suggestion == "digital art":
                response += "Digital art is awesome! Do you use any apps or draw on paper?"

            # Clear suggestion after using it
            st.session_state.last_suggestion = None

    # 🔹 2. Detect hobbies
    if not response:
        for hobby, data in hobby_data.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    detected = True
                    st.session_state.user_hobbies.append(hobby)

                    suggestion = random.choice(data["suggestions"])
                    st.session_state.last_suggestion = suggestion

                    response = (
                        f"Nice! {hobby.capitalize()} is a great hobby 😊\n\n"
                        f"💡 You might also like: **{suggestion}**\n\n"
                        f"What do you think about trying it?"
                    )
                    break
            if detected:
                break

    # 🔹 3. If user asks for suggestions
    if not response and ("suggest" in text or "idea" in text):
        if st.session_state.user_hobbies:
            hobby = random.choice(st.session_state.user_hobbies)
            suggestion = random.choice(hobby_data[hobby]["suggestions"])

            st.session_state.last_suggestion = suggestion

            response = f"Based on what you like, you could try **{suggestion}**! What do you think?"
        else:
            response = "You could try drawing, sports, or music! What sounds fun to you?"

    # 🔹 4. Greeting
    if not response and ("hello" in text or "hi" in text):
        response = "Hi! 😊 Tell me about your hobbies!"

    # 🔹 5. Fallback
    if not response:
        response = "That sounds interesting! Tell me more 😊"

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
