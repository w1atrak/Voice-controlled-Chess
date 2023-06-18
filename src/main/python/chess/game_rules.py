# from chess.piece import King, Piece
# from chess.player import Color

class GameRules:

    @staticmethod
    def transit(position, board):  #starting position, can be None
        lastMove = board.movesHistory[-1]
        color = board.get_piece(lastMove[1]).color
        x = lastMove[1][1]
        
        if color == Color.BLACK:
            if lastMove[0][0] == 1 and lastMove[1][0] == 3:
                for i in range(8):
                    if board.get_piece((3,i)) and board.get_piece((3,i)).piece_type == 'pawn' and board.get_piece((3,i)).color == Color.WHITE:
                        if position and position != GameRules.parse_tuple_position((3,i)):
                            return False
                        return GameRules.parse_tuple_position((3,i)) + ' ' + GameRules.parse_tuple_position((2,x))
        if color == Color.WHITE:
            if lastMove[0][0] == 6 and lastMove[1][0] == 4:
                for i in range(8):
                    if board.get_piece((4,i)) and board.get_piece((4,i)).piece_type == 'pawn' and board.get_piece((4,i)).color == Color.BLACK:
                        if position and position != GameRules.parse_tuple_position((4,i)):
                            return False
                        return GameRules.parse_tuple_position((4,i)) + ' ' + GameRules.parse_tuple_position((5,x))
                
        return False


    @staticmethod
    def possibleCastlings(board):
        res = []
        rightWhiteCastlingPossible = not board.white_king_made_move and ( not board.right_white_rook_made_move and GameRules.is_path_clear((7,5),(7,6),board) )
        leftWhiteCastlingPossible =  not board.white_king_made_move and ( not board.left_white_rook_made_move and GameRules.is_path_clear((7,3),(7,1),board) )

        rightBlackCastlingPossible = not board.black_king_made_move and ( not board.right_black_rook_made_move and GameRules.is_path_clear((0,5),(0,6),board) )
        leftBlackCastlingPossible =  not board.black_king_made_move and ( not board.left_black_rook_made_move and GameRules.is_path_clear((0,3),(0,1),board) )
        
        print()
        print(GameRules.is_path_clear((7,5),(7,6),board))
        board.display()
        print(board.white_king_made_move)
        print(board.right_white_rook_made_move)
        print()

        if rightWhiteCastlingPossible:
            res.append("rightWhite")
        if leftWhiteCastlingPossible:
            res.append("leftWhite")
        if rightBlackCastlingPossible:
            res.append("rightBlack")
        if leftBlackCastlingPossible:
            res.append("leftBlack")
            
        return res


    @staticmethod
    def movesThatWillResultInCheck(board, piece, position):  
        if position:
            position = GameRules.parse_str_position(position)
            moves = GameRules.available_moves(piece, position, board)
            resultMoves = []
            for move in moves:
                if GameRules.is_king_in_check_after_move(board.get_piece(move), move, position, board):
                    resultMoves.append(move)
            if len(resultMoves) == 1: return [ GameRules.parse_tuple_position(resultMoves[0]) ]
            else: return False

        if not position and piece:
            moves = []
            for i in range(8):
                for j in range(8):
                    position = GameRules.parse_tuple_position((i,j))
                    for e in GameRules.available_moves(piece, position, board):
                        moves.append(e)
            
            resultMoves = []
            
            for move in moves:
                if GameRules.is_king_in_check_after_move(piece, move, position, board):
                    resultMoves.append(move)
            if len(resultMoves) == 1: return [ GameRules.parse_tuple_position(resultMoves[0]) ]
            else: return False

        
    
    @staticmethod
    def is_path_clear(start_position, end_position, board):
        print(start_position, end_position)
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
        
        if piece.is_valid_move(start_position, end_position, board):
            # Sprawdź, czy ruch spowoduje szachowanie własnego króla
            captured_piece = board.make_move(start_position, end_position)
            is_in_check = GameRules.is_check(board, piece.color)
            board.undo_move(start_position, end_position, captured_piece)
            if is_in_check:
                return False
            return True
        return False

    
    @staticmethod
    def parse_str_position(position_str):
        position = (8 - int(position_str[1]), ord(position_str[0]) - ord('a'))
        return position
    



    @staticmethod
    def parse_tuple_position(position_tuple):
        position = chr(position_tuple[1] + ord('a')) + str(8 - position_tuple[0])
        return position

    @staticmethod
    def available_moves(piece, position, board): # end position

        moves = []
        for row in range(8):
            for col in range(8):
                piece_at_position = board.get_piece((row, col))
                if (not piece and piece_at_position)  or (piece_at_position and piece and piece.color == piece_at_position.color and piece_at_position.piece_type == piece.piece_type):
                    if GameRules.is_valid_move(piece_at_position, (row,col), GameRules.parse_str_position(position), board):
                        moves.append((row, col))
        return moves

   
    
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
                if not isinstance(piece, King):     # chyba not brakło
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



