import pygame

from chess.piece import *
from chess.board import Board
from chess.game_rules import GameRules

class ChessGUI:
    def __init__(self, board, player1, player2):
        self.board = board
        self.player1 = player1
        self.player2 = player2

        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Szachy')
        self.clock = pygame.time.Clock()

        image = pygame.image.load('src/main/resources/images/board/board.png')
        self.board_image = pygame.transform.scale(image, (800, 800))
        self.piece_images = {}
        self.load_piece_images()

    def load_piece_images(self):
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = [Color.WHITE.value, Color.BLACK.value]
        for color in colors:
            for piece in pieces:
                image = pygame.image.load(f'src/main/resources/images/pieces/{color}_{piece}.png')
                self.piece_images[f'{color}_{piece}'] = pygame.transform.scale(image, (100, 100))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()
            self.clock.tick(60)

    def draw_board(self):
        self.screen.blit(self.board_image, (0, 0))

    def draw_pieces(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece((row, col))
                if piece:
                    image = self.piece_images[f'{piece.color.value}_{piece.piece_type}']
                    x, y = col * 100, row * 100
                    self.screen.blit(image, (x, y))

