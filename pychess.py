import pygame
from constants import *
from figurset import FigureSet
from chessboard import *


class Pychess():
    def __init__(self) -> None:
        self.main()

    def main(self):
        self.setup_pygame()


    def setup_pygame(self):
        """
        setup_pygame creates the main window aswell as the layers for the chessboard and figures
        """
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.CHESSBOARD_LAYER = pygame.Surface((WIDTH, HEIGHT))
        self.FIGURE_LAYER = pygame.Surface((WIDTH,HEIGHT), pygame.SC)

        self.chessboard = Chessboard(self.CHESSBOARD_LAYER)
        self.figureset = FigureSet(self.FIGURE_LAYER)
        create_chessboard()
