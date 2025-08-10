import os

import speech_recognition as sr
import win32com.client
import webbrowser
import datetime
import pywhatkit
import openai
from Demos.EvtSubscribe_push import query_text
from pymsgbox import prompt
from soupsieve.util import lower
from wikipedia import languages


chatStr = ""

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            return "Some error occured. Sorry from Jarvis"

if __name__ == '__main__':
    print("PyCharm" )
    say("Hello i am Jarvis AI")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"], ]
        for site in sites:

            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

            elif "open music" in query.lower():
                musicPath = r"D:\Music\Banjaara.mp3"  # use raw string or double backslashes
                os.startfile(musicPath)

            elif "the time" in query.lower():
                hour = datetime.datetime.now().strftime("%H")
                min = datetime.datetime.now().strftime("%M")
                say(f"Sir, the time is {hour} hours and {minute} minutes")

            elif "open camera" in query.lower():
                os.system("start microsoft.windows.camera:")

            elif "send whatsapp" in query.lower():
                now = datetime.datetime.now()
                pywhatkit.sendwhatmsg_instantly(
                    "+918082697386",
                    "Hello from Sahil Madaan!",
                    tab_close=True,
                    close_time=2
                )

            elif "Using artificial Intelligence".lower() in query.lower():
                ai(prompt=query)

            elif "Jarvis Quit".lower() in query.lower():
                exit()

            elif "reset chat".lower() in query.lower():
                chatStr = ""

            else:
                print("Quitting...")
                # chat(query)