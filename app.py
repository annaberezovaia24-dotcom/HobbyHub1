import streamlit as st
import random

# Page settings
st.set_page_config(page_title="Hobby & Interests Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Talk with the bot about hobbies, interests, and fun activities!")

# Hobby suggestions database
hobby_responses = {
    "sports": [
        "You might enjoy playing football, basketball, or tennis! ⚽",
        "Sports are great! Have you tried swimming or cycling?",
        "Joining a local sports team can be fun and social!"
    ],
    
    "art": [
        "Art is awesome! You could try painting or sketching 🎨",
        "Digital art and animation are also cool hobbies!",
        "Watercolor painting is relaxing and creative."
    ],
    
    "music": [
        "Music is a great hobby! Do you play any instruments? 🎵",
        "You could try learning guitar, piano, or drums.",
        "Music production on a computer is also fun."
    ],
    
    "gaming": [
        "Gaming is popular! What kind of games do you like? 🎮",
        "You might enjoy game design or streaming games.",
        "Trying strategy games or puzzle games can be fun."
    ],
    
    "reading": [
        "Reading is a great hobby 📚",
        "You might enjoy fantasy, mystery, or science fiction books.",
        "Joining a book club can make reading more fun."
    ],
    
    "outdoor": [
        "Outdoor hobbies are great for health 🌳",
        "You could try hiking, camping, or photography.",
        "Nature walks and bird watching are relaxing."
    ]
}

# Default responses
default_responses = [
    "That sounds interesting! Tell me more about what you like.",
    "Cool! What hobbies are you interested in?",
    "You could try creative hobbies like drawing, music, or photography.",
    "Do you enjoy indoor hobbies or outdoor activities?"
]

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Tell me about your hobbies...")

if user_input:
    
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    user_input_lower = user_input.lower()

    response = None

    # Check keywords
    for keyword in hobby_responses:
        if keyword in user_input_lower:
            response = random.choice(hobby_responses[keyword])
            break

    # Default response if no keyword
    if not response:
        response = random.choice(default_responses)

    # Show bot message
    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
