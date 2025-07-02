import speech_recognition as sr
import os
import webbrowser
import pyttsx3
import Playlist
from dotenv import load_dotenv
import requests
from agent import agent

load_dotenv()

New_API = os.getenv('news_api')

# Rate of speech through pyttsx
engine = pyttsx3.init()
rate = engine.getProperty('rate')                       
engine.setProperty('rate', 170)

def processCommand(c):
    if "open google" in c.lower():
        speak("opening google...")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c.lower():
        speak("opening youtube...")
        webbrowser.open("https://www.youtube.com")
    elif "open facebook" in c.lower():
        speak("opening facebook...")
        webbrowser.open("https://www.facebook.com")
    elif "open instagram" in c.lower():
        speak("opening instagram...")
        webbrowser.open("https://www.instagram.com")
    elif "open linkedin" in c.lower():
        speak("opening linkedin...")
        webbrowser.open("https://www.linkedin.com")
    elif "open twitter" in c.lower():
        speak("opening twitter...")
        webbrowser.open("https://www.twitter.com")

    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = Playlist.playlists[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        speak("Getting news...")
        try:
            response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={New_API}")
            data = response.json()
            if data.get("status") == "ok":
                articles = data.get('articles', [])[:5]
                for article in articles:
                    speak(article['title'])
            else:
                speak("Sorry, couldn't fetch the news.")
        except Exception as e:
            speak("An error occurred while getting the news.")
            print(f"Error: {e}")


    
    else:
        output = agent(c)
        speak(output)
        print(output)


def speak(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Text to speech
    speak('''Initializing Jarvis..."
    How can I help you''')

    # obtain audio from the microphone
    print("recognizing")
    while True:
        # recognize speech using google_recognizer
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening...")

                audio = r.listen(source, timeout=5, phrase_time_limit=8)
                command = r.recognize_google(audio)
                print(command)

            if("jarvis" in command.lower()):
                speak("Ya")

                # listening command
                with sr.Microphone() as source:
                    print("Listening...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

            elif ("exit" in command.lower()):
                speak("Exiting Jarvis")
                break

        except Exception as e:
                        print("Waiting for your command")