# from .file import function
# git push -u origin <branch>

import speech_recognition as sr
import difflib
import re




def extractMove(results: dict):
    pieces = ["pionek", "wieża", "skoczek", "goniec", "hetman", "król"]
    matchingPieces = {x: 0 for x in pieces}
    startPos = 0
    endPos = 0

    for result in results['alternative']:

        for word in map(lambda x: x.lower(), result['transcript'].split()):
            if word in pieces: # bezpośrednie dopasowanie
                matchingPieces[word] += 1
            # else: # ból -> król, raczej eksperymentalnie
                # print(difflib.get_close_matches(word, resultPieces, cutoff=0.5))

            if re.match(r'([a-h][1-8])|([a-h]-[1-8])', word):
                if not startPos:
                    startPos = word
                elif not endPos:
                    endPos = word   
    print(results)
    print(max(matchingPieces, key=matchingPieces.get), startPos + endPos)
    return [max(matchingPieces, key=matchingPieces.get), startPos + ' ' + endPos]


def recognizeSpeech():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.3)
        print("Say something!")
        audio = r.listen(source)

    try:
        extractMove(r.recognize_google(audio, language='pl_PL', show_all=True))

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


recognizeSpeech()




