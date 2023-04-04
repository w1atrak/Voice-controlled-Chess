import copy

from chess.board import Board
from chess.player import Player

class AIPlayer(Player):
    def make_move(self, board):
        _, move = self.minimax(board, 1, float('-inf'), float('inf'), True)
        board.make_move(*move)
        return move

    def minimax(self, board, depth, alpha, beta, maximizing_player):
        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_legal_moves(board):
                new_board = Board()
                new_board.board = copy.copy(board.board)
                new_board.make_move(*move)
                eval_value, _ = self.minimax(new_board, depth - 1, alpha, beta, False)
                if eval_value > max_eval:
                    max_eval = eval_value
                    best_move = move

                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in self.get_opponent_legal_moves(board):
                new_board = Board()
                new_board.board = copy.copy(board.board)
                new_board.make_move(*move)
                eval_value, _ = self.minimax(new_board, depth - 1, alpha, beta, True)
                if eval_value < min_eval:
                    min_eval = eval_value
                    best_move = move

                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate_board(self, board):
        piece_values = {
            'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
            'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900
        }
        
        board_value = 0

        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece:
                    board_value += piece_values[piece.symbol()]

        return board_value

    def get_legal_moves(self, board):
        legal_moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == self.color:
                    for end_row in range(8):
                        for end_col in range(8):
                            if board.is_valid_move(piece, (row, col), (end_row, end_col)):
                                legal_moves.append(((row, col), (end_row, end_col)))
        return legal_moves

    def get_opponent_legal_moves(self, board):
        legal_moves = []
        opponent_color = 'white' if self.color == 'black' else 'black'
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == opponent_color:
                    for end_row in range(8):
                        for end_col in range(8):
                            if board.is_valid_move(piece, (row, col), (end_row, end_col)):
                                legal_moves.append(((row, col), (end_row, end_col)))
        return legal_moves
