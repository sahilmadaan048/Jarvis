import os
import speech_recognition as sr
import win32com.client
import webbrowser
import datetime
import pywhatkit
import requests
import random
from config import huggingface_api_key

chatStr = ""

# https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Harry: {query}\n Jarvis: "
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"]
        say(answer)
        chatStr += f"{answer}\n"
        return answer
    except Exception as e:
        print(f"Error during OpenAI request: {e}")
        say("Sorry, something went wrong while processing your request.")
        return None

def ai(prompt):
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
    headers = {"Authorization": f"Bearer {huggingface_api_key}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 256,
            "temperature": 0.7
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        output = response.json()

        if isinstance(output, list) and "generated_text" in output[0]:
            text = output[0]["generated_text"]
        else:
            text = "Sorry, I didn't get a proper response."

        if not os.path.exists("Openai"):
            os.mkdir("Openai")

        filename = f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt}\n\nResponse:\n{text}")

        print("AI response:", text)
        say(text)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except Exception as e:
        print(f"Error in ai(): {e}")

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            return "Some error occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print("PyCharm")
    say("Hello, I am Jarvis AI")
    while True:
        print("Listening...")
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"]]
        for site in sites:

            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

            elif "open music" in query.lower():
                musicPath = r"D:\Music\Banjaara.mp3"  # raw string path
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
                print("Quitting...")
                # chat(query)
