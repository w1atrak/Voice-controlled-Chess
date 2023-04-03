
import pyttsx3

def change_voice(engine, language):
    for voice in engine.getProperty('voices'):
        if language in voice.languages :
            engine.setProperty('voice', voice.id)
            return True



def speak(text):
    engine = pyttsx3.init()
    change_voice(engine, 'pl_PL')  
    engine.say(text)
    engine.runAndWait()

