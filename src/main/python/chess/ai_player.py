import copy
import random
import time

from chess.board import Board
from chess.player import Player, Color
from chess.game_rules import GameRules

class AIPlayerMC(Player):
    def __init__(self, color, time_limit=2, max_moves=100):
        super().__init__(color)
        self.time_limit = time_limit
        self.max_moves = max_moves

    def make_move(self, board):
        start_time = time.time()
        possible_moves = self.get_possible_moves(board)
        move_scores = {move: 0 for move in possible_moves}

        while time.time() - start_time < self.time_limit:
            for move in possible_moves:
                simulated_board = copy.deepcopy(board)
                self.simulate_move(simulated_board, move)
                for _ in range(10):
                    winner = self.simulate_game(simulated_board, self.max_moves)
                    if winner == self.color:
                        move_scores[move] += 1

        best_move = max(move_scores, key=move_scores.get)
        board.make_move(*best_move)

    def get_possible_moves(self, board):
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece and piece.color == self.color:
                    for end_row in range(8):
                        for end_col in range(8):
                            if board.is_valid_move(piece, (row, col), (end_row, end_col)):
                                possible_moves.append(((row, col), (end_row, end_col)))
        return possible_moves

    def simulate_move(self, board, move):
        start, end = move
        piece = board.get_piece(start)
        board.make_move(start, end)
        return board

    def simulate_game(self, board, max_moves):
        current_color = self.color
        moves = 0
        while moves < max_moves:
            possible_moves = self.get_possible_moves(board)
            if not possible_moves:
                return Color.BLACK if current_color == Color.WHITE else Color.WHITE
            move = random.choice(possible_moves)
            board.make_move(*move)
            current_color = Color.BLACK if current_color == Color.WHITE else Color.WHITE
            moves += 1
        return None

class AIPlayer(Player):
    def make_move(self, board):
        _, move = self.minimax(board, 3, float('-inf'), float('inf'), True, Color.BLACK)
        board.make_move(*move)
        return move

    def minimax(self, board, depth, alpha, beta, maximizing_player, color):
        if depth == 0: # or board.is_game_over():
            return self.evaluate_board(board, color), None

        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_legal_moves(board):
                new_board = Board()
                new_board.board = copy.deepcopy(board.board)
                new_board.make_move(*move)
                eval_value, _ = self.minimax(new_board, depth - 1, alpha, beta, False, self.color if maximizing_player else Color.WHITE if self.color == Color.BLACK else Color.BLACK)
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
                new_board.board = copy.deepcopy(board.board)
                new_board.make_move(*move)
                eval_value, _ = self.minimax(new_board, depth - 1, alpha, beta, True, self.color if maximizing_player else Color.WHITE if self.color == Color.BLACK else Color.BLACK)
                if eval_value < min_eval:
                    min_eval = eval_value
                    best_move = move

                beta = min(beta, eval_value)
                if beta <= alpha:
                    break
            return min_eval, best_move


    # def evaluate_board(self, board, color):
    #     piece_values = {
    #         'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
    #         'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900
    #     }
        
    #     board_value = 0

    #     for row in range(8):
    #         for col in range(8):
    #             piece = board.get_piece((row, col))
    #             if piece:
    #                 board_value += piece_values[piece.symbol()]

    #     if color == Color.BLACK:
    #         board_value *= -1

    #     return board_value

    def evaluate_board(self, board, color):
        piece_values = {
            'P': 10, 'N': 30, 'B': 30, 'R': 50, 'Q': 90, 'K': 900,
            'p': -10, 'n': -30, 'b': -30, 'r': -50, 'q': -90, 'k': -900
        }
        
        position_values = {
            'P': [[0, 0, 0, 0, 0, 0, 0, 0],
                [5, 5, 5, 5, 5, 5, 5, 5],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
                [0, 0, 0, 2, 2, 0, 0, 0],
                [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
                [0.5, 1, 1, -2, -2, 1, 1, 0.5],
                [0, 0, 0, 0, 0, 0, 0, 0]],
            'N': [[-5, -4, -3, -3, -3, -3, -4, -5],
                [-4, -2,  0,  0,  0,  0, -2, -4],
                [-3,  0,  1,  1.5, 1.5,  1,  0, -3],
                [-3, 0.5, 1.5,  2,  2, 1.5, 0.5, -3],
                [-3,  0, 1.5,  2,  2, 1.5,  0, -3],
                [-3, 0.5,  1,  1.5, 1.5,  1, 0.5, -3],
                [-4, -2,  0, 0.5, 0.5,  0, -2, -4],
                [-5, -4, -3, -3, -3, -3, -4, -5]],
            'B': [[-2, -1, -1, -1, -1, -1, -1, -2],
                [-1,  0,  0,  0,  0,  0,  0, -1],
                [-1,  0, 0.5,  1,  1, 0.5,  0, -1],
                [-1, 0.5, 0.5,  1,  1, 0.5, 0.5, -1],
                [-1,  0, 1,  1,  1,  1,  0, -1],
                [-1,  1, 1,  1,  1,  1,  1, -1],
                [-1,  0, 0,  0,  0,  0,  0, -1],
                [-2, -1, -1, -1, -1, -1, -1, -2]],
            'R': [[0, 0, 0, 0, 0, 0, 0, 0],
                [0.5, 1, 1, 1, 1, 1, 1, 0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
                [0, 0, 0, 0.5, 0.5, 0, 0, 0]],
            'Q': [[-2, -1, -1, -0.5, -0.5, -1, -1, -2],
                [-1, 0, 0, 0, 0, 0, 0, -1],
                [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
                [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
                [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
                [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
                [-1, 0, 0, 0, 0, 0, 0, -1],
                [-2, -1, -1, -0.5, -0.5, -1, -1, -2]],
            'K': [[-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-3, -4, -4, -5, -5, -4, -4, -3],
                [-2, -3, -3, -4, -4, -3, -3, -2],
                [-1, -2, -2, -2, -2, -2, -2, -1],
                [2, 2, 0, 0, 0, 0, 2, 2],
                [2, 3, 1, 0, 0, 1, 3, 2]]
        }


        
        board_value = 0

        for row in range(8):
            for col in range(8):
                piece = board.get_piece((row, col))
                if piece:
                    board_value += piece_values[piece.symbol()]
                    if piece.symbol().upper() in position_values:
                        if piece.color == Color.WHITE:
                            board_value += position_values[piece.symbol().upper()][row][col]
                        else: # if the piece is black, we need to reverse the board
                            board_value -= position_values[piece.symbol().upper()][7-row][col]

        if color == Color.BLACK:
            board_value *= -1

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
                                new_board = copy.deepcopy(board)
                                new_board.make_move((row, col), (end_row, end_col))
                                if not GameRules.is_check(new_board, self.color):
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
                                new_board = copy.deepcopy(board)
                                new_board.make_move((row, col), (end_row, end_col))
                                if not GameRules.is_check(new_board, opponent_color):
                                    legal_moves.append(((row, col), (end_row, end_col)))
        return legal_moves

