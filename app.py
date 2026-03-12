def chatbot_response(user_input):
    user_input = user_input.lower()

    art_words = ["art", "painting", "drawing", "sketch"]
    music_words = ["music", "guitar", "piano", "sing"]
    coding_words = ["coding", "programming", "python", "software"]
    sports_words = ["sports", "football", "basketball", "tennis"]

    if any(word in user_input for word in art_words):
        return "🎨 Art is a creative hobby! Try painting, drawing, or digital art."

    elif any(word in user_input for word in music_words):
        return "🎵 Music is amazing! You can learn instruments or music production."

    elif any(word in user_input for word in coding_words):
        return "💻 Coding lets you build apps, websites, and games!"

    elif any(word in user_input for word in sports_words):
        return "⚽ Sports keep you active! Football, basketball, swimming and more!"

    elif "hobby" in user_input or "suggest" in user_input:
        return """Here are some hobbies you can try:
        
🎨 Art – drawing, painting  
🎵 Music – guitar, piano  
💻 Coding – build apps or games  
⚽ Sports – football, swimming  
📚 Reading – explore new ideas"""

    elif "hello" in user_input or "hi" in user_input:
        return "Hi there! 👋 Welcome to HobbyHub!"

    elif "bye" in user_input:
        return "Goodbye! Come back soon 😊"

    else:
        return "That sounds interesting! Tell me more!"
