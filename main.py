import speech_recognition as sr
import win32com.client

def say(text):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio)
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            return "Some error occured. Sorry from Jarvis"

if __name__ == '__main__':
    print("PyCharm" )
    say("Hello i am Jarvis AI")
    while True:
        print("Listening...")
        text = takeCommand()
        say(text)

