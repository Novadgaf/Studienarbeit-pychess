from matplotlib.pyplot import draw
from tile import Tile
from constants import *
import pygame

class Chessboard():
    def __init__(self, screen) -> None:
        self.SURFACE = screen
        self.create_board()


    def create_board(self):
        """
        create_board draws / resets chessboard
        """
        
        for col in range(8):
            for row in range(8):
                if col % 2 == 0:
                    color = COLOR_BLACK
                else:
                    color = COLOR_WHITE
                self.draw_tile(color, col, row)
        pygame.display.update()
    

    def draw_tile(self, color: str, cord_y: int, cord_x: int) -> None:
        """
        draw_tile draws a single color rectangle

        Args:
            color (str): color of the rectangle
            cord_y (int): y cord of the rect (0-7)
            cord_x (int): x cord of the rect (0-7)
        """
        pygame.draw.rect(self.SURFACE, color, [SQUARE_SIZE*cord_x, SQUARE_SIZE*cord_y, SQUARE_SIZE, SQUARE_SIZE])