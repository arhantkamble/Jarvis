import pyttsx3
from decouple import config
import speech_recognition as sr
from datetime import datetime
from random import choice
from utils import opening_text

# Load configuration
USERNAME = config('USER', default='User')
BOTNAME = config('BOTNAME', default='Jarvis')

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 190)
engine.setProperty('volume', 1.0)

# Select Voice
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  # Female voice
else:
    engine.setProperty('voice', voices[0].id)  # Default voice

def speak(text):
    """Converts text to speech."""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greets the user based on the time of day."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning, {USERNAME}!")
    elif 12 <= hour < 16:
        speak(f"Good Afternoon, {USERNAME}!")
    elif 16 <= hour < 19:
        speak(f"Good Evening, {USERNAME}!")
    speak(f"I am {BOTNAME}. How may I assist you?")

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
        if query in ["exit", "stop", "quit", "bye"]:
            hour = datetime.now().hour
            if 21 <= hour or hour < 6:
                speak("Good night, take care!")
            else:
                speak("Have a great day ahead!")
            break
        elif query != "None":
            speak(choice(opening_text))

if __name__ == "__main__":
    main()