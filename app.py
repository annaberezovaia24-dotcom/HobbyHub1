import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's chat about your hobbies and discover new ones!")

# Expanded hobby database
hobby_data = {
    "drawing": ["drawing", "sketching", "art"],
    "swimming": ["swim", "swimming"],
    "tennis": ["tennis"],
    "reading": ["read", "books", "reading"],
    "gaming": ["gaming", "games"],
    "music": ["music", "singing"],
    "sports": ["football", "basketball", "sports"],
}

# Suggestions
suggestions = {
    "drawing": "You could try digital art or painting 🎨",
    "swimming": "You might enjoy water polo or diving 🌊",
    "tennis": "You could also try badminton or table tennis 🎾",
    "reading": "You might enjoy writing your own stories 📚",
    "gaming": "Maybe try game design or streaming 🎮",
    "music": "Learning an instrument could be fun 🎵",
    "sports": "You could explore different team sports ⚽"
}

# Conversation memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_hobbies" not in st.session_state:
    st.session_state.user_hobbies = []

# Show chat history
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

    found = []

    # Detect hobbies
    for hobby, keywords in hobby_data.items():
        for word in keywords:
            if word in text:
                found.append(hobby)

    response = ""

    # CASE 1: User mentions hobbies
    if found:
        st.session_state.user_hobbies.extend(found)

        responses = []
        for hobby in found:
            responses.append(f"{hobby.capitalize()} sounds fun! 😊")

        follow_up = random.choice([
            "What do you enjoy most about it?",
            "How often do you do it?",
            "How did you get into it?"
        ])

        response = " ".join(responses) + " " + follow_up

    # CASE 2: User asks for suggestions
    elif "suggest" in text or "recommend" in text:
        if st.session_state.user_hobbies:
            hobby = random.choice(st.session_state.user_hobbies)
            response = suggestions.get(hobby, "You could try something creative or active!")
        else:
            response = random.choice([
                "You could try drawing, sports, or music!",
                "Maybe explore gaming, reading, or outdoor activities!",
                "How about learning a new skill like coding or photography?"
            ])

    # CASE 3: Greeting
    elif "hello" in text or "hi" in text:
        response = random.choice([
            "Hi there! 😊 What hobbies do you enjoy?",
            "Hello! 👋 Tell me about what you like to do!",
        ])

    # CASE 4: General fallback
    else:
        response = random.choice([
            "That sounds interesting! Tell me more 😊",
            "Nice! What else do you enjoy?",
            "Cool! Do you have any other hobbies?"
        ])

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
