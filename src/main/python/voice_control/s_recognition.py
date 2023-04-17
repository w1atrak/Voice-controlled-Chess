
import speech_recognition as sr
import re
from voice_control.s_synthesis import speak
from chess.game_rules import *

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



def extractMove(results, board, savedMatchings = {}): 
    if not results or not results['alternative']:
        return None
    print(results)

    keyWords = ["pionek", "pion", 
                "wieża", "wieżę", 
                "skoczek", "skoczka", 
                "goniec", "gońca", 
                "hetman", "hetmana", 
                "król", "króla", 
                "roszada", "krótka", "długa", 
                "przelot", "przelocie", 
                "bicie", "biję", "bije", 
                "szach", 
                "prom", "promowanie", "przemiana", "awans", "koronacja", "hetmanowanie", "promuję", "promuje"]
    pieces = ["pionek", "pion","wieża", "skoczek", "goniec", "hetman", "król"]
    # roszadaWords = ["krótka", "długa"]                 #
    promWords = ["wieża", "skoczek", "goniec", "hetman", "wieżę", "skoczka", "gońca", "hetmana"]

    matchings = {x: 0 for x in keyWords}

    for word in savedMatchings:
        matchings[word] += 1
    

    positions = ''
    positionsInterpreted = -1
    
    for result in results['alternative']:

        result = string_NumbersToNumbers(result['transcript'])
        result = cutSpaces(result)

        startPos = ''
        endPos = ''

        for word in map(lambda x: x.lower(), result.split()):
            if word in keyWords: 
                matchings[word] += 1
            
            if re.match(r'([a-h][1-8])', word):
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
    # piecesWords = ["pionek", "pion", "wieża", "wieżę", "skoczek", "skoczka", "goniec", "gońca", "hetman", "hetmana", "król"]


    piece = ""
    if matchings["pionek"] > 0 or matchings["pion"] > 0:
        piece = "pawn"
    elif matchings["wieża"] > 0 or matchings["wieżę"] > 0:
        piece = "rook"
    elif matchings["skoczek"] > 0 or matchings["skoczka"] > 0:
        piece = "knight"
    elif matchings["goniec"] > 0 or matchings["gońca"] > 0:
        piece = "bishop"
    elif matchings["hetman"] > 0 or matchings["hetmana"] > 0:
        piece = "queen"
    elif matchings["król"] > 0 or matchings["króla"] > 0:
        piece = "king"

        
#
    if matchings['roszada']:
        if board.king_made_move or ( board.left_rook_made_move and board.right_rook_made_move ):
            speak("roszada nie jest możliwa")
            return extractMove(recognizeSpeech(), board)
        
        rightCastlingPossible = not board.right_rook_made_move and GameRules.is_path_clear((7,5),(7,6),board)
        leftCastlingPossible = not board.left_rook_made_move and GameRules.is_path_clear((7,3),(7,1),board)

        if matchings['krótka']:
            if not rightCastlingPossible:
                speak("roszada krótka nie jest możliwa")
                return extractMove(recognizeSpeech(), board)    
            else:
                return "e1 g1"
            
        if matchings['długa']:
            if not leftCastlingPossible:
                speak("roszada długa nie jest możliwa")
                return extractMove(recognizeSpeech(), board)
            else:
                return "e1 c1"
            
        if leftCastlingPossible:
            speak("roszada długa")
            return "e1 c1"
        elif rightCastlingPossible:
            speak("roszada krótka")
            return "e1 g1"

        else:
            speak("roszada nie jest możliwa")
            
#TODO
    elif matchings['przelot']   or matchings['przelocie']  :
        speak("bicie w przelocie")
        # czy jakakolwiek możliwa z ewentualnymi pozycjami

#TODO
    elif matchings['bicie']   or matchings['biję']   or matchings['bije']  :
        speak("bicie")
        # czy jakiekolwiek możliwe z ewentualnymi pozycjami

#TODO
    elif matchings['szach']  :
        speak("szach")
        # czy jakikolwiek możliwy z ewentualnymi pozycjami

#TODO prom 1
    elif matchings['koronacja'] or matchings['hetmanowanie']:
        speak("koronacja, promowanie na hetmana")
        # czy jakakolwiek możliwa z ewentualnymi pozycjami

#TODO prom 2
    elif matchings['prom']   or matchings['promowanie']   or matchings['przemiana']   or matchings['awans']   or matchings['promuję']   or matchings['promuje']  :
        for piece in promWords:
            if matchings[piece]  :
                speak("promowanie na " + piece)
                break 
        else:
            speak("Doprecyzuj na co promować")
            extractMove( recognizeSpeech(), ["promowanie"])


    else:
        if positionsInterpreted == 1:   # ruch na tą pozycję, ewentualnie danego pionka
            speak(positions)
            speak(piece)
            moves = GameRules.available_moves(piece, positions, board)
            print(moves,"174 s_reco")
            if len(moves) == 1:
                result_pos = GameRules.parse_tuple_position(moves[0]) + ' ' + positions
                print(result_pos)
                return result_pos
                
            else:
                speak("Zaproponowany ruch jest niejednoznaczny lub niepoprawny, proszę o doprecyzowanie")
                return extractMove( recognizeSpeech(), board )
        elif positionsInterpreted == 2:
            speak(positions)
            return positions



    return None







def recognizeSpeech():

    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.3)
            print("Say something!")
            audio = r.listen(source)

        try:
            return r.recognize_google(audio, language='pl_PL', show_all=True)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))



def getMoveFromSpeech(board):
    return extractMove(recognizeSpeech(), board)




