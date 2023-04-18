from enum import Enum

class Color(Enum):
    WHITE = 'white'
    BLACK = 'black'

class Player:
    def __init__(self, color: Color):
        self.color = color
#add types to make_move arguments
    def make_move(self, board, move):
        # move to krotka (start_position, end_position), np. ((0, 1), (2, 1)) 
        # TODO: pamiętać o dodaniu typów
        start_position, end_position = move
        piece = board.get_piece(start_position)
        
        if not piece or piece.color != self.color:
            return False

        if board.is_valid_move(piece, start_position, end_position):
            board.make_move(start_position, end_position)
            return True
        else:
            return False
