import streamlit as st

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's talk about hobbies and discover new interests!")

# Hobby knowledge base
hobby_data = {
    "reading": {
        "response": "Reading is a great hobby 📚. What type of books do you enjoy?",
        "suggestion": "You might also enjoy writing stories or joining a book club."
    },
    "tennis": {
        "response": "Tennis is an awesome sport 🎾. Do you usually play for fun or competitively?",
        "suggestion": "You might also enjoy badminton or table tennis."
    },
    "drawing": {
        "response": "Drawing is very creative ✏️. Do you prefer sketching people, landscapes, or cartoons?",
        "suggestion": "You might enjoy digital art or painting too."
    },
    "gaming": {
        "response": "Gaming is fun 🎮. What kind of games do you usually play?",
        "suggestion": "You could also try game design or streaming."
    },
    "music": {
        "response": "Music is a great hobby 🎵. Do you play an instrument or just enjoy listening?",
        "suggestion": "Learning guitar or piano could be fun."
    }
}

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_hobbies" not in st.session_state:
    st.session_state.user_hobbies = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Tell me about your hobbies...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    text = user_input.lower()

    found_hobbies = []

    # Detect hobbies in message
    for hobby in hobby_data:
        if hobby in text:
            found_hobbies.append(hobby)

    response = ""

    # If hobbies found
    if found_hobbies:
        st.session_state.user_hobbies.extend(found_hobbies)

        responses = []
        for hobby in found_hobbies:
            responses.append(hobby_data[hobby]["response"])

        response = " ".join(responses)

    # If user talks about free time
    elif "free time" in text:
        if st.session_state.user_hobbies:
            response = f"Earlier you mentioned you enjoy {', '.join(st.session_state.user_hobbies)}. What do you like most about it?"
        else:
            response = "What hobbies do you usually enjoy in your free time?"

    # Greetings
    elif "hello" in text or "hi" in text:
        response = "Hi there! 😊 What hobbies do you enjoy?"

    else:
        response = "That sounds interesting! Can you tell me more about your hobbies?"

    # Show bot reply
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
