from chess.piece import *
from chess.game_rules import GameRules
from chess.player import Player, Color
from voice_control.s_recognition import requestPromFigure
import json, os


class Board:

    white_king_made_move = False
    black_king_made_move = False
    left_white_rook_made_move = False
    right_white_rook_made_move = False
    left_black_rook_made_move = False
    right_black_rook_made_move = False
    movesHistory = [((-1,-1),(-1,-1))]
    player2 = None
    value = 0
    
    
    requestedPromotionFigure = None

    def __init__(self, custom = False, customPath = 'config.json'):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.custom = custom
        self.customPath = customPath
        self.setup_pieces()

    def __str__(self):
        return self.get_string()

    def display(self):
        print(self.get_string())

    def get_string(self):
        board_str = ''
        for row in self.board:
            board_str += ' '.join([str(piece) if piece else '.' for piece in row]) + '\n'
        return board_str
            
    def get_piece(self, position):
        row, col = position
        return self.board[row][col]

    def is_valid_move(self, piece, start_position, end_position):
        if GameRules.is_king_in_check_after_move(piece, start_position, end_position, self):
            return False
        
        return GameRules.is_valid_move(piece, start_position, end_position, self)

    def make_move(self, start_position, end_position):
        start_row, start_col = start_position
        end_row, end_col = end_position
        captured_piece = self.board[end_row][end_col]
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
        return captured_piece
    
    def undo_move(self, start_position, end_position, captured_piece):
        start_row, start_col = start_position
        end_row, end_col = end_position
        self.board[start_row][start_col] = self.board[end_row][end_col]
        self.board[end_row][end_col] = captured_piece
        
        

    def find_king(self, king_color):
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if piece and piece.color == king_color and isinstance(piece, King):  # poprawiony warunek
                    king_position = (row, col)
                    break
            if king_position:
                break
        return king_position

    def setup_pieces(self):
        
        if not self.custom:
            for row, color in [(0, Color.BLACK), (7, Color.WHITE)]:
                self.board[row] = [
                    Rook(color),
                    Knight(color),
                    Bishop(color),
                    Queen(color),
                    King(color),
                    Bishop(color),
                    Knight(color),
                    Rook(color)
                ]

            for row, color in [(1, Color.BLACK), (6, Color.WHITE)]:
                for col in range(8):
                    self.board[row][col] = Pawn(color)
        else:
            with open(os.path.abspath('./src/main/resources/config/' + self.customPath)) as f:
                data = json.load(f)
                
                for figure in data['white']:
                    self.board[figure[1]][figure[2]] = eval(figure[0] + '(Color.WHITE)')  # poprawiony eval
                    
                for figure in data['black']:
                    self.board[figure[1]][figure[2]] = eval(figure[0] + '(Color.BLACK)')  # poprawiony eval



    def specialMoves(self, player):
        if len(self.movesHistory) == 1: return False

        lastMove = self.movesHistory[-1]
        startPos = lastMove[0] 
        endPos = lastMove[1]
        if isinstance(self.get_piece(endPos), King):
            if endPos == (7,6) and startPos == (7,4):
                player.make_move(self, ((7,7),(7,5)))
                self.movesHistory.pop()
                self.movesHistory.append([(7,4),(7,6), None,(7,7),(7,5), None])
                
                return "h1 f1"
            if endPos == (7,2) and startPos == (7,4):
                player.make_move(self, ((7,0),(7,3)))
                return "a1 d1"
            
        
        # promowanie po ruchu pionka na ostatnie pole
        if not endPos[0] and isinstance(self.get_piece(endPos), Pawn):
            if not self.requestedPromotionFigure:
                requestPromFigure(self)
            self.board[endPos[0]][endPos[1]] = self.requestedPromotionFigure
            self.requestedPromotionFigure = None
        
        return None
    
    def evaluate_board(self):
        piece_values = {
            Pawn: 10, Knight: 30, Bishop: 30, Rook: 50, Queen: 90, King: 900,
        }
        
        board_value = 0

        for row in range(8):
            for col in range(8):
                piece = self.get_piece((row, col))
                if piece:
                    board_value += piece_values[type(piece)] * (1 if piece.color == Color.WHITE else -1)  # poprawiona wartość

        return board_value
    
    def getBoardValue(self):
        return self.evaluate_board()

    def provideHintMove(self):
        bestMove = None
        bestVal = float('inf')
        for startRow in range(8):
            for startCol in range(8):
                piece = self.get_piece((startRow, startCol))
                if piece and piece.color == Color.WHITE:
                    for endRow in range(8):
                        for endCol in range(8):
                            if self.is_valid_move(piece, (startRow, startCol), (endRow, endCol)):
                                taken = self[endRow][endCol]
                                self[endRow][endCol] = piece
                                self[startRow][startCol] = None
                                val = self.getBoardValue(self) 
                                if val < bestVal:
                                    bestVal = val
                                    bestMove = [(startRow, startCol), (endRow, endCol)]
                                self.undo_move((startRow, startCol), (endRow, endCol), taken)
        if bestMove:
            return GameRules.parse_tuple_position(bestMove[0]) + ' ' + GameRules.parse_tuple_position(bestMove[1])
        return None            
                                