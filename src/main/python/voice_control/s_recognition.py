
import speech_recognition as sr
import re
from voice_control.s_synthesis import speak

# git push -u origin <branch>



def string_NumbersToNumbers(s):  
    return s.replace('jeden', '1').replace('dwa', '2').replace('trzy', '3').replace('cztery', '4').replace('pięć', '5').replace('sześć', '6').replace('siedem', '7').replace('osiem', '8')


def cutSpaces(result):
    removed = 0
    for index, char in enumerate(result):
        if char.isdigit() and len(result) > 2: 
            index -= removed           # and > or 
            if ( index == 2 or index > 2 and result[index-3].isspace()  ) and ( ( result[index-1].isspace() or result[index-1] == "-" ) and result[index-2].isalpha() ) :
                    result = result[:index-1] + result[index:]   
                    removed += 1
            if ( index == len(result) - 3 or index < len(result) - 3 and result[index+3].isspace()  ) and ( ( result[index+1].isspace() or result[index+1] == "-") and result[index+2].isalpha() ) :
                    result = result[:index+1] + result[index+2:]   
                    removed += 1
                    result = result[:index] + result[index+1] + result[index] + result[index+2:]  # 8c -> c8
 
    return result



def extractMove(results, savedMatchings = {}): 
    if not results or not results['alternative']:
        return None
    

    keyWords = ["pionek", "pion", "wieża", "wieżę", "skoczek", "skoczka", "goniec", "gońca", "hetman", "hetmana", "król", 
                "roszada", "krótka", "długa", 
                "przelot", "przelocie", 
                "bicie", "biję", "bije", 
                "szach", 
                "prom", "promowanie", "przemiana", "awans", "koronacja", "hetmanowanie", "promuję", "promuje"]                                  #   # roszadaWords = ["krótka", "długa"]                 #
    promWords = ["wieża", "skoczek", "goniec", "hetman", "wieżę", "skoczka", "gońca", "hetmana"]
    pieces = ["pionek", "pion", "wieża", "skoczek", "goniec", "hetman", "król"]
    
    matchings = {x: 0 for x in keyWords}

    for word in savedMatchings:
        matchings[word] += 1
    

    positions = ''
    positionsInterpreted = -1
    mainPiece = None
    
    for result in results['alternative']:

        result = string_NumbersToNumbers(result['transcript'])
        result = cutSpaces(result)

        startPos = ''
        endPos = ''

        for word in map(lambda x: x.lower(), result.split()):
            if word in keyWords: 
                matchings[word] += 1
            
            if word in pieces and not mainPiece:
                mainPiece = word
            
            if re.match(r'(^[a-h][1-8]$)', word):
                if not startPos:
                    startPos = word
                elif not endPos:
                    endPos = word  

        if startPos and endPos:
            positions = startPos + ' ' + endPos
            positionsInterpreted = 2
        elif startPos and not endPos and positionsInterpreted < 2:
            positions = startPos
            positionsInterpreted = 1
        elif not startPos:
            positionsInterpreted = 0



        
#
    if matchings['roszada']  :    ################## roszadę
        if matchings['krótka']  :
            # roszada krótka
            speak("roszada krótka")
        elif matchings['długa']  :
            # roszada długa
            speak("roszada długa")
        else:
            speak("za mało danych o roszadzie")
            # czy jakakolwiek możliwa
            
# 
    elif matchings['przelot']   or matchings['przelocie']  :
        speak("bicie w przelocie")
        # czy jakakolwiek możliwa z ewentualnymi pozycjami

#
    elif matchings['bicie']   or matchings['biję']   or matchings['bije']  :
        speak("bicie")
        # czy jakiekolwiek możliwe z ewentualnymi pozycjami

#
    elif matchings['szach']  :
        speak("szach")
        # czy jakikolwiek możliwy z ewentualnymi pozycjami

#
    elif matchings['koronacja'] or matchings['hetmanowanie']:
        speak("koronacja, promowanie na hetmana")
        # czy jakakolwiek możliwa z ewentualnymi pozycjami

#
    elif matchings['prom']   or matchings['promowanie']   or matchings['przemiana']   or matchings['awans']   or matchings['promuję']   or matchings['promuje']  :
        for piece in promWords:
            if matchings[piece]  :
                speak("promowanie na " + piece)
                break 
        else:
            speak("Doprecyzuj na co promować")
            extractMove( recognizeSpeech(), ["promowanie"])

    elif positions:
    # sprawdzenie możliwych ruchów ze względu na pozycje
        speak(positions)

# 
    else:
        speak("nie rozpoznano ruchu")

    print(positions)
    return None







def recognizeSpeech():

    r = sr.Recognizer()
    print(sr.Microphone())
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
    try:
        return r.recognize_google(audio, language='pl_PL', show_all=True)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

