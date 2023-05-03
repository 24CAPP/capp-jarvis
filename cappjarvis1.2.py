import json
import openai
import speech_recognition as sr
from gtts import gTTS
from playsound import playsound

with open("secrets.json") as f:
    secrets = json.load(f)
    api_key = secrets["api_key"]

openai.api_key = api_key

r = sr.Recognizer()

def speak(text):
    language = 'it'
    myobj = gTTS(text=text, lang=language, slow=False)
    myobj.save("response.mp3")
    playsound("response.mp3")

def get_audio():
    with sr.Microphone() as source:
        print("Parla ora...")
        audio = r.listen(source)
        try:
            user_input = r.recognize_google(audio, language="it-IT")
            print(f"Tu: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Non ho capito, ripeti per favore...")
            return ""
        except sr.RequestError as e:
            print(f"Errore nella richiesta a Google Speech Recognition: {e}")
            return ""

def get_response(messages:str):
    response = openai.Completion.create(
        engine = "text-davinci-002",
        prompt = f"{messages}\nTu:",
        temperature = 0.7,
        max_tokens = 1024,
        n = 1,
        stop = "Capp:"
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    messages = "Ciao sono Capp Jervis 1.0, Daje roma daje iniziamo."
    try:
        print(f"Capp: {messages}")
        speak(messages)
        while True:
            user_input = get_audio()
            if user_input:
                messages += f"\nUtente: {user_input}\nCapp:"
                response = get_response(messages)
                print(f"Capp: {response}")
                speak(response)
                messages += f" {response}"
    except KeyboardInterrupt:
        print("A presto!")
