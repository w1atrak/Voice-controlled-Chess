from chess.piece import Piece
from chess.game_rules import GameRules

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
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
                if piece and piece.color == king_color and piece.piece_type == 'king':
                    king_position = (row, col)
                    break
            if king_position:
                break
        return king_position

    def setup_pieces(self):
        for row, color in [(0, 'black'), (7, 'white')]:
            self.board[row] = [
                Piece('rook', color),
                Piece('knight', color),
                Piece('bishop', color),
                Piece('queen', color),
                Piece('king', color),
                Piece('bishop', color),
                Piece('knight', color),
                Piece('rook', color)
            ]

        for row, color in [(1, 'black'), (6, 'white')]:
            for col in range(8):
                self.board[row][col] = Piece('pawn', color)
