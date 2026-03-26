import streamlit as st
import random

st.set_page_config(page_title="Hobby Chatbot", page_icon="🎨")

st.title("🎨 Hobby & Interests Chatbot")
st.write("Tell me what you like, or ask me to suggest hobbies!")

# ✅ UPDATED HOBBY DATA (NEW VOCABULARY ADDED)
hobby_data = {
    "sports": {
        "keywords": ["tennis", "football", "basketball", "cycling", "padel", "running", "swimming"],
        "similar": ["badminton", "volleyball", "table tennis", "hiking", "skateboarding"],
        "response": "Nice! You seem to enjoy sports 💪"
    },
    "creative": {
        "keywords": ["draw", "drawing", "painting", "sketch", "art"],
        "similar": ["digital art", "animation", "illustration", "graphic design", "crafting"],
        "response": "That's awesome! You're creative 🎨"
    },
    "science": {
        "keywords": ["science", "experiment", "physics", "chemistry", "biology"],
        "similar": ["robotics", "coding", "astronomy", "engineering projects", "lab experiments"],
        "response": "Very interesting! You like learning 🔬"
    },
    "music": {
        "keywords": ["music", "guitar", "piano", "sing", "singing"],
        "similar": ["drums", "ukulele", "songwriting", "music production", "djing"],
        "response": "Nice! Music is a great hobby 🎵"
    },
    "math": {
        "keywords": ["math", "mathematics", "numbers", "algebra"],
        "similar": ["puzzles", "chess", "sudoku", "coding", "logic games"],
        "response": "Awesome! You enjoy thinking and solving problems 🧠"
    },
    "adventure": {
        "keywords": ["climbing", "hiking", "mountain", "camping"],
        "similar": ["rock climbing", "trail running", "kayaking", "cycling", "backpacking"],
        "response": "Wow! You love adventure and the outdoors 🧗"
    },
    "winter": {
        "keywords": ["ice skating", "skating", "skiing", "snowboarding"],
        "similar": ["figure skating", "hockey", "sledding", "ice hockey"],
        "response": "That’s cool! You enjoy winter activities ❄️"
    },
    "reading": {
        "keywords": ["reading", "books", "novels", "stories"],
        "similar": ["writing", "blogging", "poetry", "storytelling"],
        "response": "Nice! Reading is a great way to learn and relax 📚"
    },
    "gaming": {
        "keywords": ["gaming", "games", "video games", "minecraft", "fortnite"],
        "similar": ["game development", "coding", "streaming", "esports"],
        "response": "Fun! Gaming can be really exciting 🎮"
    }
}

# Instrument suggestions
instruments = ["guitar", "piano", "drums", "ukulele", "violin"]

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

    # 1. Greetings
    if any(word in text for word in ["hi", "hello", "hey"]):
        response = random.choice(greetings)

    # 2. Ask for suggestions
    elif any(phrase in text for phrase in ["suggest", "recommend", "give me ideas", "any hobby"]):
        category = random.choice(list(hobby_data.keys()))
        data = hobby_data[category]

        suggestions = random.sample(data["similar"], min(3, len(data["similar"])))

        st.session_state.last_category = category
        st.session_state.last_suggestions = suggestions

        response = "Of course! 😊 Here are some hobby ideas:\n\n💡 You could try:\n"
        for s in suggestions:
            response += f"- **{s}**\n"
        response += "\nDo any of these sound interesting?"

    # 3. MORE IDEAS
    elif any(phrase in text for phrase in ["more", "more ideas", "something else", "another", "anything else"]):
        category = st.session_state.last_category

        if category:
            data = hobby_data[category]

            available = [
                h for h in data["similar"]
                if h not in st.session_state.last_suggestions
                and h not in st.session_state.rejected
            ]

            if not available:
                available = data["similar"]

            new_suggestions = random.sample(available, min(3, len(available)))
            st.session_state.last_suggestions = new_suggestions

            response = "Sure! 😊 Here are some more ideas:\n\n💡 You could also try:\n"
            for s in new_suggestions:
                response += f"- **{s}**\n"
            response += "\nDo any of these sound interesting?"
        else:
            response = "Tell me a hobby you like first 😊"

    # 4. Dislike
    elif any(word in text for word in ["don't like", "do not like", "hate", "dislike"]):
        category = st.session_state.last_category

        if category:
            st.session_state.rejected.extend(st.session_state.last_suggestions)

            available = [
                h for h in hobby_data[category]["similar"]
                if h not in st.session_state.rejected
            ]

            if not available:
                available = hobby_data[category]["similar"]

            new_suggestions = random.sample(available, min(3, len(available)))
            st.session_state.last_suggestions = new_suggestions

            response = "No worries 😊 Try these instead:\n\n"
            for s in new_suggestions:
                response += f"- **{s}**\n"
        else:
            response = "No problem 😊 What do you prefer?"

    # 5. Instrument suggestions
    elif "instrument" in text:
        available = [i for i in instruments if i not in st.session_state.last_suggestions]
        if not available:
            available = instruments

        suggestions = random.sample(available, min(3, len(available)))
        st.session_state.last_suggestions = suggestions
        st.session_state.last_category = "music"

        response = "🎵 You could try these instruments:\n\n"
        for s in suggestions:
            response += f"- **{s}**\n"

    # 6. Detect hobby
    else:
        for category, data in hobby_data.items():
            for keyword in data["keywords"]:
                if keyword in text:
                    detected = True
                    st.session_state.last_category = category

                    available = [
                        h for h in data["similar"]
                        if h not in st.session_state.rejected
                    ]

                    if not available:
                        available = data["similar"]

                    suggestions = random.sample(available, min(3, len(available)))
                    st.session_state.last_suggestions = suggestions

                    response = f"{data['response']} 😊\n\n💡 You might also enjoy:\n"
                    for s in suggestions:
                        response += f"- **{s}**\n"

                    response += "\nWhich one sounds interesting?"
                    break
            if detected:
                break

    # 7. Fallback
    if not response:
        response = random.choice([
            "That sounds interesting! 😊 Tell me more!",
            "Nice! What hobbies do you enjoy?",
            "Cool! Tell me more about that!"
        ])

    # Show response
    with st.chat_message("assistant"):
        st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
