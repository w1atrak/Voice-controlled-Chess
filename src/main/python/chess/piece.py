from chess.player import Color

class Piece:
    def __init__(self, color: Color):
        self.color = color 
        self.piece_type = ''

    def __str__(self):
        return self.symbol()

class Pawn(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'pawn'

    def symbol(self):
        return 'P' if self.color == Color.WHITE else 'p'

class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'knight'

    def symbol(self):
        return 'N' if self.color == Color.WHITE else 'n'

class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'bishop'

    def symbol(self):
        return 'B' if self.color == Color.WHITE else 'b'

class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'rook'

    def symbol(self):
        return 'R' if self.color == Color.WHITE else 'r'

class Queen(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'queen'

    def symbol(self):
        return 'Q' if self.color == Color.WHITE else 'q'

class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'king'

    def symbol(self):
        return 'K' if self.color == Color.WHITE else 'k'
