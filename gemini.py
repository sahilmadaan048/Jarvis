import os
from csv import excel
from http.cookiejar import split_header_words

import speech_recognition as sr
import  win32com.client
import webbrowser
import datetime
import pywhatkit
import requests
import random

from aiohttp import payload_type

from config import GEMINI_API_KEY


chatStr = ""

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def chat(query):
    global chatStr
    print(chatStr)

    chatStr += f"User: {query}\nJarvis: "
    try:
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        payload = {
            "contents": [
                {"parts": [{"text": chatStr}]}
            ]
        }

        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        answer = data["candidates"][0]["content"]["parts"][0]["text"]

        # say(answer)
        chatStr += f"{answer}\n"
        return answer
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        say("Sorry, something went wrong while processing your request.")
        return None

def ai(prompt):
    try:
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ]
        }

        response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        text = data["candidates"][0]["content"]["parts"][0]["text"]

        if not os.path.exists("Gemini"):
            os.mkdir("Gemini")

        filename = f"Gemini/{''.join(prompt.split()[:5])}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt}\n\nResponse:\n{text}")

        print("AI response:", text)
        # say(text)

    except Exception as e:
        print(f"Error in ai(): {e}")


def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Some error occurred: {e}")
            return None


if __name__ == "__main__":
    print("Pycharm")
    say("hello, I am JARVIS AI")
    while True:
        print("Listening...")
        query = takeCommand()
        if not query:
            continue

        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]

        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

            elif "open music" in query.lower():
                musicPath = r"D:\Music\Banjaara.mp3"
                os.startfile(musicPath)

            elif "the time" in query.lower():
                hour = datetime.datetime.now().strftime("%H")
                minute = datetime.datetime.now().strftime("%M")
                say(f"Sir, the time is {hour} hours and {minute} minutes")

            elif "open camera" in query.lower():
                os.system("start microsoft.windows.camera:")

            elif "send whatsapp" in query.lower():
                pywhatkit.sendwhatmsg_instantly(
                    "+918082697386",
                    "Hello from Sahil Madaan!",
                    tab_close=True,
                    close_time=2
                )

            elif "using artificial intelligence" in query.lower():
                ai(prompt=query)

            elif "jarvis quit" in query.lower():
                exit()

            elif "reset chat" in query.lower():
                chatStr = ""

            else:
                print("Chatting...")
                chat(query)



# pip install speechRecongition
# pip install wikipedia
# import webBrowser wala is used to access the wb vrowser from the