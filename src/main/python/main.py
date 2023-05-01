import sys
import pygame
import threading

from chess.board import Board
from chess.player import Color, Player
from chess.ai_player import AIPlayer
from chess.random_ai_player import RandomAIPlayer
from chess.game_rules import GameRules
from chess.gui import ChessGUI

from voice_control.s_recognition import *
from commentary.commentator import *

def game_logic(gui, player1, player2, board):
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break
        # board.CheckIfLastMoveWasSpecial()
        if board.movesHistory[-1] == ((7,4),(7,6)):
            speak("czas na wieżę")
            move = "h1 f1"
        # else:
        #     move = getMoveFromSpeech(board)
        # if not move:
        #     continue
        
        gui.draw_board()
        gui.draw_pieces()
        pygame.display.flip()

        #print(board)
        move = input("Podaj swój ruch (np. 'e2 e4'): ")
        #move = extractMove(recognizeSpeech())
        start_position, end_position = parse_move(move)
        print(start_position, end_position)
        if player1.make_move(board, (start_position, end_position)):
            print("Poprawny ruch!")
            speak(getComment(move[3:]))
            board.movesHistory.append((start_position, end_position))
        else:
            print("Niepoprawny ruch, spróbuj ponownie.")
            continue

        gui.draw_board()
        gui.draw_pieces()
        pygame.display.flip()

        if GameRules.is_checkmate(board, player2.color):
            print("Szach-mat! Wygrywasz.")
            game_over = True
            break
        elif GameRules.is_stalemate(board, player2.color):
            print("Pat! Remis.")
            game_over = True
            break

        ai_move = player2.make_move(board)
        print(f"AI wykonało ruch: {format_move(ai_move)}")

        if GameRules.is_checkmate(board, player1.color):
            print("Szach-mat! Wygrywa AI.")
            game_over = True
            break
        elif GameRules.is_stalemate(board, player1.color):
            print("Pat! Remis.")
            game_over = True
            break

def main():
    board = Board()
    player1 = Player(Color.WHITE)
    player2 = RandomAIPlayer(Color.BLACK)
    gui = ChessGUI(board, player1, player2)

    game_logic_thread = threading.Thread(target=game_logic, args=(gui, player1, player2, board))
    game_logic_thread.start()

    gui.run()

    game_logic_thread.join()


def parse_move(move_str):
    start_str, end_str = move_str.strip().split()
    start_position = (8 - int(start_str[1]), ord(start_str[0]) - ord('a'))
    end_position = (8 - int(end_str[1]), ord(end_str[0]) - ord('a'))
    return start_position, end_position



def format_move(move):
    start_position, end_position = move
    start_str = f"{chr(ord('a') + start_position[1])}{8 - start_position[0]}"
    end_str = f"{chr(ord('a') + end_position[1])}{8 - end_position[0]}"
    return f"{start_str} {end_str}"

if __name__ == "__main__":
    main()
