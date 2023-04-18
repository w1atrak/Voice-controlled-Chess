class GameRules:
    @staticmethod
    def is_path_clear(start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        row_diff = end_row - start_row
        col_diff = end_col - start_col

        row_step = 0 if row_diff == 0 else (1 if row_diff > 0 else -1)
        col_step = 0 if col_diff == 0 else (1 if col_diff > 0 else -1)

        current_row = start_row + row_step
        current_col = start_col + col_step

        while current_row != end_row or current_col != end_col:
            if board.get_piece((current_row, current_col)):
                return False
            current_row += row_step
            current_col += col_step

        return True

    @staticmethod
    def is_in_bounds(position):
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8

    @staticmethod
    def is_valid_move(piece, start_position, end_position, board):
        if not end_position:
            return False
        
        if start_position == end_position:
            return False
        
        if not GameRules.is_in_bounds(end_position):
            return False
        
        destination_piece = board.get_piece(end_position)
        if destination_piece and destination_piece.color == piece.color:
            return False
        
        if isinstance(piece, Pawn):
            return GameRules.is_valid_pawn_move(piece, start_position, end_position, board)
        elif isinstance(piece, Rook):
            return GameRules.is_valid_rook_move(piece, start_position, end_position, board)
        elif isinstance(piece, Bishop):
            return GameRules.is_valid_bishop_move(piece, start_position, end_position, board)
        elif isinstance(piece, Queen):
            return GameRules.is_valid_queen_move(piece, start_position, end_position, board)
        elif isinstance(piece, King):
            return GameRules.is_valid_king_move(piece, start_position, end_position, board)
        elif isinstance(piece, Knight):
            return GameRules.is_valid_knight_move(piece, start_position, end_position, board)

        return False

    @staticmethod
    def is_valid_pawn_move(piece, start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        row_diff = end_row - start_row
        col_diff = abs(end_col - start_col)

        if piece.color == Color.WHITE:
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
            if row_diff == direction and board.get_piece(end_position) and board.get_piece(end_position).color != piece.color:
                return True
        return False

    @staticmethod
    def is_valid_rook_move(piece, start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        if start_row != end_row and start_col != end_col:
            return False
        return GameRules.is_path_clear(start_position, end_position, board)

    @staticmethod
    def is_valid_bishop_move(piece, start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        return GameRules.is_path_clear(start_position, end_position, board)

    @staticmethod
    def is_valid_queen_move(piece, start_position, end_position, board):
        return GameRules.is_valid_rook_move(piece, start_position, end_position, board) or \
               GameRules.is_valid_bishop_move(piece, start_position, end_position, board)

    @staticmethod
    def is_valid_king_move(piece, start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if row_diff <= 1 and col_diff <= 1:
            return True
        return False

    @staticmethod
    def is_valid_knight_move(piece, start_position, end_position, board):
        start_row, start_col = start_position
        end_row, end_col = end_position
        row_diff = abs(start_row - end_row)
        col_diff = abs(start_col - end_col)
        if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
            return True
        return False
    
    @staticmethod
    def is_king_in_check_after_move(piece, start_position, end_position, board):
        captured_piece = board.make_move(start_position, end_position)
        is_in_check = GameRules.is_check(board, piece.color)
        board.undo_move(start_position, end_position, captured_piece)
        return is_in_check

    @staticmethod
    def is_check(board, king_color):
        king_position = board.find_king(king_color)

        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color != king_color:
                    if GameRules.is_valid_move(piece, (row, col), king_position, board):
                        return True
        return False

    @staticmethod
    def is_checkmate(board, king_color):
        if not GameRules.is_check(board, king_color):
            return False

        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == king_color:
                    start_position = (row, col)
                    for end_row in range(8):
                        for end_col in range(8):
                            end_position = (end_row, end_col)
                            if GameRules.is_valid_move(piece, start_position, end_position, board) and not GameRules.is_king_in_check_after_move(piece, start_position, end_position, board):
                                return False
        return True

    @staticmethod
    def only_kings_left(board):
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if isinstance(piece, King):
                    return False
        return True

    @staticmethod
    def is_stalemate(board, king_color):
        if GameRules.is_check(board, king_color):
            return False
        
        if GameRules.only_kings_left(board):
            return True

        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == king_color:
                    start_position = (row, col)
                    for end_row in range(8):
                        for end_col in range(8):
                            end_position = (end_row, end_col)
                            if GameRules.is_valid_move(piece, start_position, end_position, board) and not GameRules.is_king_in_check_after_move(piece, start_position, end_position, board):
                                return False
        return True

