class Piece:
    def __init__(self, piece_type, color):
        self.piece_type = piece_type
        self.color = color

    def __str__(self):
        if self.color == 'white':
            return self.piece_type[0].upper()
        else:
            return self.piece_type[0].lower()