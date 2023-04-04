class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color

    def __str__(self):
        char = 'n' if self.piece_type == 'knight' else self.piece_type[0]
        if self.color == 'white':
            return char.upper()
        else:
            return char.lower()