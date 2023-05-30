import pygame

from chess.piece import *
from chess.board import Board
from chess.game_rules import GameRules

import speech_recognition

class ChessGUI:
    def __init__(self, board, player1, player2, recognizer):
        self.board = board
        self.player1 = player1
        self.player2 = player2
        self.recognizer = recognizer

        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Szachy')
        self.clock = pygame.time.Clock()

        image = pygame.image.load('src/main/resources/images/board/board.png')
        self.board_image = pygame.transform.scale(image, (800, 800))
        self.piece_images = {}
        self.load_piece_images()

        image = pygame.image.load('src/main/resources/images/misc/mic_icon.png')
        self.mic_icon = pygame.transform.scale(image, (100, 100))
        self.mic_icon.set_alpha(128) 


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
            self.draw_marks()

            if self.recognizer.is_listening:
                self.screen.blit(self.mic_icon, (350, 350))

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
    
    def draw_marks(self):
        font = pygame.font.Font(None, 32)
        r = 15
        for i in range(8):
            circle_surface = pygame.Surface((2*r, 2*r), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (64, 64, 64, 196), (r, r), r)  # 128 is the level of transparency

            self.screen.blit(circle_surface, (20 - 7.5, i * 100 + 35 - 5))  # subtracting 20 to center the circle
            text = font.render(str(8 - i), True, (32, 225, 255)) 
            self.screen.blit(text, (20, i * 100 + 35)) 

            circle_surface = pygame.Surface((2*r, 2*r), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, (64, 64, 64, 196), (r, r), r)  # 128 is the level of transparency

            self.screen.blit(circle_surface, (i * 100 + 45 - 10, 765 - 5))  # subtracting 20 to center the circle
            text = font.render(chr(97 + i), True, (32, 225, 255)) 
            self.screen.blit(text, (i * 100 + 45, 765))




