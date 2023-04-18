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
            if piece.piece_type == 'king':
                board.king_made_move = True
            if piece.piece_type == 'rook':
                if start_position == (7, 0):
                    board.left_rook_made_move = True
                if start_position == (7,7):
                    board.right_rook_made_move = True
            return True
        else:
            return False
