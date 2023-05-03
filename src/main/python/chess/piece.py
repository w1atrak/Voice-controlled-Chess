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
    
    def is_valid_move(self, start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        row_diff = end_row - start_row
        col_diff = abs(end_col - start_col)

        if self.color == Color.WHITE:
            direction = -1
            initial_row = 6
        else:
            direction = 1
            initial_row = 1

        if col_diff == 0:
            if row_diff == direction and not board.get_piece(end_position):
                return True
            if start_row == initial_row and row_diff == 2 * direction and not board.get_piece(end_position) and not board.get_piece((start_row + direction, start_col)):
                return True
        elif col_diff == 1:
            if row_diff == direction and board.get_piece(end_position) and board.get_piece(end_position).color != self.color:
                return True
        return False

class Knight(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'knight'

    def symbol(self):
        return 'N' if self.color == Color.WHITE else 'n'
    
    def is_valid_move(self, start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
        return False

class Bishop(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'bishop'

    def symbol(self):
        return 'B' if self.color == Color.WHITE else 'b'
    
    def is_valid_move(self, start_position, end_position, board):
        from chess.game_rules import GameRules

        start_row, start_col = start_position
        end_row, end_col = end_position
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        return GameRules.is_path_clear(start_position, end_position, board)

class Rook(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'rook'

    def symbol(self):
        return 'R' if self.color == Color.WHITE else 'r'
    
    def is_valid_move(self, start_position, end_position, board):
        from chess.game_rules import GameRules

        start_row, start_col = start_position
        end_row, end_col = end_position
        if start_row != end_row and start_col != end_col:
            return False
        if isinstance(board.get_piece(board.movesHistory[-1][1]), King):
            if start_position == (7,7) and end_position == (7,5) and board.movesHistory[-1] == ((7,4),(7,6)): 
                return not board.right_white_rook_made_move
            if start_position == (7,0) and end_position == (7,3) and board.movesHistory[-1] == ((7,4),(7,2)): 
                return not board.left_white_rook_made_move
            
        return GameRules.is_path_clear(start_position, end_position, board)


class Queen(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'queen'

    def symbol(self):
        return 'Q' if self.color == Color.WHITE else 'q'
    
    def is_valid_move(self, start_position, end_position, board):
        rook = Rook(self.color)
        bishop = Bishop(self.color)

        return rook.is_valid_move(start_position, end_position, board) or \
                bishop.is_valid_move(start_position, end_position, board)
    


class King(Piece):
    def __init__(self, color: Color):
        super().__init__(color)
        self.piece_type = 'king'

    def symbol(self):
        return 'K' if self.color == Color.WHITE else 'k'

    def is_valid_move(self, start_position, end_position, board):
        from chess.game_rules import GameRules

        start_row, start_col = start_position
        end_row, end_col = end_position
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if row_diff <= 1 and col_diff <= 1:
            board.white_king_made_move = True
            return True
        if GameRules.parse_tuple_position(start_position) == "e1":
            if GameRules.parse_tuple_position(end_position) == "g1" and "rightWhite" in GameRules.possibleCastlings(board):
                board.white_king_made_move = True
                return True
            if GameRules.parse_tuple_position(end_position) == "c1" and "leftWhite" in GameRules.possibleCastlings(board):
                board.white_king_made_move = True
                return True

        return False