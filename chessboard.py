from typing import Tuple
from constants import *
import pygame
from figures import *
from os import walk

class Chessboard():
    def __init__(self, board_surface: pygame.Surface, figure_surface: pygame.Surface, fen: str = STARTFEN) -> None:
        self.BOARD_SURFACE = board_surface
        self.FIGURE_SURFACE = figure_surface
        self.IMAGES = self.loadFigureImages()
        self.color_to_move = "white"
        self.create_board(fen)
        

    def create_board(self, fen):
        """
        create_board creates board from fen

        Args:
            fen (str): fen string with board position
        """
        self.draw_board()
        self.squares = self.loadPositionFromFenString(fen)
        self.draw_figures()

        
    def draw_board(self):
        """
        draw_board draws chessboard
        """
        for col in range(8):
            for row in range(8):
                if (col+row) % 2 != 0:
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
        pygame.draw.rect(self.BOARD_SURFACE, color, [SQUARE_SIZE*cord_x, SQUARE_SIZE*cord_y, SQUARE_SIZE, SQUARE_SIZE])


    def loadFigureImages(self) -> dict:
        """
        loadFigureImages loads all figure images into a dictionary

        Returns:
            dict: dictionary containing an image for each figure
        """

        filenames = next(walk(r"./images"), (None, None, []))[2]  # [] if no file
        images = {}
        for filename in filenames:
            path = fr"images/{filename}"

            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

            images[filename] = img

        return images


    def draw_figure(self, cord_x: int, cord_y: int, figure: Figure) -> None:
        """
        draw_figure draws a single figure

        Args:
            cord_x (int): x pos to draw
            cord_y (int): y pos to draw
            figure (Figure): figure to draw
        """

        rec = pygame.Rect(cord_x,cord_y,SQUARE_SIZE,SQUARE_SIZE)
        self.FIGURE_SURFACE.blit(self.IMAGES[figure.NAME], rec)


    def draw_figures(self):
        """
        draw_figures draws all figures from a given list
        """
        for idx, figure in enumerate(self.squares):
            if figure == None:
                continue
            file = idx % 8
            rank = int(idx/8)
            
            cord_x = file*SQUARE_SIZE
            cord_y = rank*SQUARE_SIZE

            self.draw_figure(cord_x, cord_y, figure)

        pygame.display.update()

    def get_square_under_mouse(self) -> Tuple:
        """
        get_square_under_mouse gets the x, y position of the mouse and the piece underneeth

        Args:
            board_surface (pygame.Surface): Chessboard Surface

        Returns:
            Tuple: x and y coordinate 
        """
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        pos_x, pos_y = [int(v // SQUARE_SIZE) for v in mouse_pos]

        if 8 > pos_x >= 0 and 8 > pos_y >= 0: return (pos_x, pos_y, self.squares[pos_y*8 + pos_x])

        return (None, None)

    def draw_drag(self, figure) -> None:
        if figure == None:
            return
        
        pos = pygame.Vector2(pygame.mouse.get_pos())
        self.draw_figure(pos[0]-0.5*SQUARE_SIZE, pos[1]-0.5*SQUARE_SIZE, figure)


    def loadPositionFromFenString(self, fen: str) -> list[Figure]:

        symbolPieceDic = {
            "p": Pawn,
            "r": Rook,
            "n": Knight,
            "b": Bishop,
            "q": Queen,
            "k": King
        }

        chessboard_array: Figure = [None for x in range(64)]

        file = 0
        rank = 0
        
        position = fen.split(" ")[0]

        for symbol in position:
            if symbol == "/":
                file = 0
                rank = rank+1
                continue

            if symbol.isnumeric():
                file += int(symbol)
            else:
                color = "black" if symbol.islower() else "white"
                piece = symbolPieceDic[symbol.lower()](color)
                chessboard_array[rank*8 + file] = piece
                file += 1
                

        return chessboard_array