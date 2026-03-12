import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Let's talk about hobbies and discover new interests!")

# Hobby database
hobbies = {
    "art": ["painting", "drawing", "digital art", "watercolor"],
    "music": ["guitar", "piano", "singing", "music production"],
    "sports": ["football", "basketball", "cycling", "swimming"],
    "gaming": ["strategy games", "puzzle games", "RPG games"],
    "reading": ["fantasy books", "mystery novels", "science fiction"],
    "outdoor": ["hiking", "camping", "photography", "bird watching"],
    "tech": ["coding", "robotics", "game development"]
}

# Store conversation state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "topic" not in st.session_state:
    st.session_state.topic = None

# Display chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
user_input = st.chat_input("Tell me about your hobbies...")

if user_input:

    st.session_state.messages.append({"role":"user","content":user_input})
    with st.chat_message("user"):
        st.write(user_input)

    text = user_input.lower()
    response = ""

    # Detect hobby topics
    for key in hobbies:
        if key in text:
            st.session_state.topic = key

    # Conversation logic
    if "hello" in text or "hi" in text:
        response = "Hi there! 😊 What hobbies do you enjoy?"

    elif st.session_state.topic:
        hobby_list = hobbies[st.session_state.topic]
        suggestion = random.choice(hobby_list)

        response = f"Nice! {st.session_state.topic.capitalize()} is a great hobby area. You might enjoy **{suggestion}**. Have you ever tried it?"

    elif "bored" in text:
        response = "If you're bored, trying a new hobby can help! Do you prefer creative hobbies, sports, tech, or outdoor activities?"

    elif "yes" in text:
        response = "Awesome! What part of that hobby do you enjoy the most?"

    elif "no" in text:
        response = "No worries! Maybe we can find something new for you. Do you like creative things, sports, or technology?"

    else:
        response = "That sounds interesting! Tell me more about what you enjoy doing in your free time."

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role":"assistant","content":response})
