
import speech_recognition as sr
import re
from voice_control.s_synthesis import speak
from chess.game_rules import *
from chess.piece import *




def string_NumbersToNumbers(s):  
    return s.replace('jeden', '1').replace('dwa', '2').replace('trzy', '3').replace('cztery', '4').replace('pięć', '5').replace('sześć', '6').replace('siedem', '7').replace('osiem', '8')


def cutSpaces(result):
    removed = 0
    for index, char in enumerate(result):
        if char.isdigit() and len(result) > 2: 
            index -= removed           
            if ( index == 2 or index > 2 and result[index-3].isspace()  ) and ( ( result[index-1].isspace() or result[index-1] == "-" ) and result[index-2].isalpha() ) :
                    result = result[:index-1] + result[index:]   
                    removed += 1
            if ( index == len(result) - 3 or index < len(result) - 3 and result[index+3].isspace()  ) and ( ( result[index+1].isspace() or result[index+1] == "-") and result[index+2].isalpha() ) :
                    result = result[:index+1] + result[index+2:]   
                    removed += 1
                    result = result[:index] + result[index+1] + result[index] + result[index+2:]  # 8c -> c8
 
    return result



def extractKeyWords(results, board, savedMatchings = []): 
    if not results or not results['alternative']:
        return None
    print(results, "s_reco/extractKeyWords")

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
    pieces = ["pionek", "pion", "wieża", "skoczek", "goniec", "hetman", "król"]
    
    matchings = {x: 0 for x in keyWords}

    for word in savedMatchings:
        matchings[word] += 1
    

    positions = ''
    positionsInterpreted = 0
    
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
                    positionsInterpreted = 1
                elif not endPos :
                    positionsInterpreted = 2
                    endPos = word  
                print(word, startPos, endPos, "word")

        if startPos and endPos:
            positions = startPos + ' ' + endPos
            positionsInterpreted = 2
        elif startPos and not endPos and positionsInterpreted < 2:
            positions = startPos
            positionsInterpreted = 1

    # piecesWords = ["pionek", "pion", "wieża", "wieżę", "skoczek", "skoczka", "goniec", "gońca", "hetman", "hetmana", "król"]


    piece = None
    if matchings["pionek"] > 0 or matchings["pion"] > 0:
        piece = Pawn(Color.WHITE)
    elif matchings["wieża"] > 0 or matchings["wieżę"] > 0:
        piece = Rook(Color.WHITE)
    elif matchings["skoczek"] > 0 or matchings["skoczka"] > 0:
        piece = Knight(Color.WHITE)
    elif matchings["goniec"] > 0 or matchings["gońca"] > 0:
        piece = Bishop(Color.WHITE)
    elif matchings["hetman"] > 0 or matchings["hetmana"] > 0:
        piece = Queen(Color.WHITE)
    elif matchings["król"] > 0 or matchings["króla"] > 0:
        piece = King(Color.WHITE)

    print(positionsInterpreted, "pos")
    return analyzeKeyWords(matchings, board, positionsInterpreted, positions, piece)
        



def analyzeKeyWords(matchings, board, positionsInterpreted,positions, piece):
#
    if positionsInterpreted == 2:
        speak(positions)
        return positions

#
    promWords = ["wieża", "skoczek", "goniec", "hetman", "wieżę", "skoczka", "gońca", "hetmana"]

    if matchings['roszada']:
        if board.white_king_made_move or ( board.left_white_rook_made_move and board.right_white_rook_made_move ):
            speak("roszada nie jest możliwa")
            return extractKeyWords(recognizeSpeech(), board)
        
        castlings = GameRules.possibleCastlings(board)

        if matchings['krótka']:
            if not "rightWhite" in castlings:
                speak("roszada krótka nie jest możliwa")
                return extractKeyWords(recognizeSpeech(), board)    
            else:
                speak("roszada krótka")
                return "e1 g1"
            
        if matchings['długa']:
            if not "leftWhite" in castlings:
                speak("roszada długa nie jest możliwa")
                return extractKeyWords(recognizeSpeech(), board)
            else:
                speak("roszada długa")
                return "e1 c1"
            
        if "leftWhite" in castlings and not "rightWhite" in castlings:
            speak("roszada długa")
            return "e1 c1"
        elif "rightWhite" in castlings and not "leftWhite" in castlings:
            speak("roszada krótka")
            return "e1 g1"

        else:
            speak("roszada nie jednoznacza")
            
    elif matchings['przelot']   or matchings['przelocie']  :
        speak("bicie w przelocie")
        res = GameRules.transit(positions, board)
        if not res:
            speak("nie ma takiego przelotu")
            return extractKeyWords(recognizeSpeech(), board)
        else:
            return res




    elif matchings['szach']:
      
        res = GameRules.movesThatWillResultInCheck(board, piece, positions)
        if not res: 
            return extractKeyWords(recognizeSpeech(), board)
        if len(res) == 1:
            return res[0] + " " + positions




    elif matchings['koronacja'] or matchings['hetmanowanie']:
        speak("koronacja")
        board.requestedPromotionFigure = Queen(Color.WHITE)
        # czy jakakolwiek możliwa z ewentualnymi pozycjami

    elif matchings['prom']   or matchings['promowanie']   or matchings['przemiana']   or matchings['awans']   or matchings['promuję']   or matchings['promuje']:

        if piece:
            board.requestedPromotionFigure = piece
            speak("promowanie na " + piece.symbol())
            
        else:
            speak("Doprecyzuj na co promować")
            extractKeyWords( recognizeSpeech(), ["promowanie"])


#
    if positionsInterpreted == 1:   # ruch na tą pozycję, ewentualnie danego pionka
        print("x")
        speak(positions)
        moves = GameRules.available_moves(piece, positions, board)
        if len(moves) == 1:
            result_pos = GameRules.parse_tuple_position(moves[0]) + ' ' + positions
            print(result_pos)
            return result_pos
            
        else:
            speak("Zaproponowany ruch jest niejednoznaczny lub niepoprawny, proszę o doprecyzowanie")
            return extractKeyWords( recognizeSpeech(), board )

# 
    else:
        speak("nie rozpoznano ruchu")

    speak("Nie zrozumiano ruchu, proszę o więcej informacji")
    return None


def requestPromFigure():
    matchings = {"prom" : 1}
    return analyzeKeyWords(matchings, board=None,positionsInterpreted=0,positions=None,piece=None)




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



def getMoveFromSpeech(board):
    return extractKeyWords(recognizeSpeech(), board)




