import pyttsx3
from decouple import config
import speech_recognition as sr
from datetime import datetime
from random import choice
import os
import webbrowser
from utils import opening_text

# Load configuration
USERNAME = config('USER', default='User')
BOTNAME = config('BOTNAME', default='Jarvis')

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 120)
engine.setProperty('volume', 1.0)

# Select Voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greets the user based on the time of day."""
    hour = datetime.now().hour
    greeting = "Good Morning" if 6 <= hour < 12 else "Good Afternoon" if 12 <= hour < 16 else "Good Evening"
    speak(f"{greeting}, {USERNAME}! I am {BOTNAME}. How may I assist you?")

def take_user_input():
    """Listens to user input, converts speech to text, and handles errors."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5)
            print('Recognizing...')
            query = r.recognize_google(audio, language='en-in').lower()
            print(f"User said: {query}")
        except sr.WaitTimeoutError:
            speak("No input detected. Please try again.")
            return "None"
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Could you say that again?")
            return "None"
        except sr.RequestError:
            speak("I'm having trouble connecting to the speech service.")
            return "None"
    return query

def main():
    """Main function to run the assistant in a loop."""
    greet_user()
    
    while True:
        query = take_user_input()

        # Exit conditions
        if query in ["exit", "stop", "quit", "bye"]:
            speak("Good night, take care!" if 21 <= datetime.now().hour or datetime.now().hour < 6 else "Have a great day ahead!")
            break

        # Greetings
        elif query in ["how are you", "how are you doing", "how r u"]:
            speak("I am good! Thank you for asking. How about you?")

        # Time query
        elif query in ["what time is it", "tell me the time", "current time"]:
            current_time = datetime.now().strftime("%I:%M %p")  # Example: 10:45 AM
            speak(f"The current time is {current_time}")

        # Date query
        elif query in ["what's the date today", "tell me today's date", "current date", "the date today"]:
            current_date = datetime.now().strftime("%A, %B %d, %Y")  # Example: Wednesday, March 12, 2025
            speak(f"Today's date is {current_date}")

        # Introduce itself
        elif query in ["who are you", "what is your name"]:
            speak(f"My name is {BOTNAME}. I am your virtual assistant!")

        # Joke
        elif query in ["tell me a joke", "make me laugh"]:
            jokes = [
                "Why don’t skeletons fight each other? Because they don’t have the guts!",
                "Why did the computer catch a cold? Because it left its Windows open!",
                "Why don’t some couples go to the gym? Because some relationships don’t work out!"
            ]
            speak(choice(jokes))

        # Open applications
        elif query in ["open notepad"]:
            os.system("notepad.exe")
            speak("Opening Notepad.")
        elif query in ["open calculator"]:
            os.system("calc.exe")
            speak("Opening Calculator.")
        elif query in ["open command prompt", "open cmd"]:
            os.system("start cmd")
            speak("Opening Command Prompt.")
        elif query in ["open whatsapp"]:
            os.system("WhatsApp.exe")
            speak("Opening whatsapp.")

        # Google Search
        elif "search for" in query:
            search_query = query.replace("search for", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"Searching Google for {search_query}")

        # Weather Inquiry (Placeholder, real implementation requires API)
        elif query in ["what's the weather", "how's the weather today"]:
            speak("I can't fetch live weather updates yet, but you can check it on Google.")
            webbrowser.open("https://www.google.com/search?q=weather")

        # Motivational Quotes
        elif query in ["give me a quote", "tell me a motivational quote"]:
            quotes = [
                "The only way to do great work is to love what you do. – Steve Jobs",
                "Believe you can and you're halfway there. – Theodore Roosevelt",
                "It does not matter how slowly you go as long as you do not stop. – Confucius"
            ]
            speak(choice(quotes))

        # Default response from opening_text
        elif query.strip():  # Ensures non-empty input
            speak(choice(opening_text))

if __name__ == "__main__":
    main()
