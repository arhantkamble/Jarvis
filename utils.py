import random

opening_text = [
    "How can I assist you?",
    "What would you like me to do?",
    "How may I help you today?"
]

def get_random_opening():
    return random.choice(opening_text)
