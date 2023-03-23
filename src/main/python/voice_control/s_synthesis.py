# import gtts
# from playsound import playsound
# tts = gtts.gTTS(text='Witam w szachach ', lang='pl')
# tts.save("welcome.mp3")


import pyttsx3
def change_voice(engine, language):
    for voice in engine.getProperty('voices'):
        if language in voice.languages :
            engine.setProperty('voice', voice.id)
            return True


engine = pyttsx3.init()
change_voice(engine, 'pl_PL')
txt = "W Szczebrzeszynie chrząszcz brzmi w trzcinie"
engine.say(txt)
engine.runAndWait()