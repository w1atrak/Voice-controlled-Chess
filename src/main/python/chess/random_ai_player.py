import random

from chess.player import Player

class RandomAIPlayer(Player):
    movesHistory = []
    
    def make_move(self, board):
        move = random.choice(self.get_legal_moves(board))
        piece = board.make_move(*move)
        self.movesHistory.append((move[0], move[1], piece))
        return move
    
    def undoMove(self, board):
        lastMove = self.movesHistory.pop()
        board.undo_move(lastMove[0], lastMove[1], lastMove[2])


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