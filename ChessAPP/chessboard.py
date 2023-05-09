from typing import Tuple
from constants import *
import pygame
from figures import *
from os import walk
import copy

class Chessboard():
    def __init__(self, board_surface: pygame.Surface, figure_surface: pygame.Surface, fen: str = STARTFEN) -> None:
        self.BOARD_SURFACE = board_surface
        self.FIGURE_SURFACE = figure_surface
        self.IMAGES = self.loadFigureImages()

        #0 for white 1 for black
        self.color_to_move = 0b0
        self.castle_right = "KQkq"
        self.en_passant_square = "-"
        self.saved_state = None
        self.create_board(fen)
        
    def save_state(self):
        state = {
            'color_to_move': self.color_to_move,
            'castle_right': self.castle_right,
            'en_passant_square': self.en_passant_square,
            'squares': copy.deepcopy(self.squares),
            'saved_state': copy.deepcopy(self.saved_state)
        }
        self.saved_state = state

    def make_move(self, move: Move):
        self.save_state()
        self.color_to_move = self.color_to_move^0b1
        self.en_passant_square = move.EN_PASSANT_SQUARE

        if move.IS_CASTLE:
            self.castle(move.CASTLE_TYPE)
            return

        if move.CAPTURE != None:
            self.squares[move.CAPTURE] = None
        self.squares[move.START_SQUARE] = None
        self.squares[move.END_SQUARE] = move.FIGURE
        self.squares[move.END_SQUARE].has_moved = True

    def restore_state(self):
        if self.saved_state:
            self.color_to_move = self.saved_state['color_to_move']
            self.castle_right = self.saved_state['castle_right']
            self.en_passant_square = self.saved_state['en_passant_square']
            self.squares = self.saved_state['squares']
            self.saved_state = self.saved_state['saved_state']
        else:
            print("No saved state available.")

    def castle(self, type):
        print(f"castle type {type} rights {self.castle_right}")
        if type == "K" and type in self.castle_right:
            king = self.squares[self.square_name_to_index("e1")]
            rook = self.squares[self.square_name_to_index("h1")]

            self.squares[self.square_name_to_index("g1")] = king
            self.squares[self.square_name_to_index("f1")] = rook
            self.squares[self.square_name_to_index("g1")].has_moved = True
            self.squares[self.square_name_to_index("f1")].has_moved = True
            self.squares[self.square_name_to_index("e1")] = None
            self.squares[self.square_name_to_index("h1")] = None
            self.castle_right = self.castle_right.replace(type, "")
            pass
        elif type == "Q" and type in self.castle_right:
            king = self.squares[self.square_name_to_index("e1")]
            rook = self.squares[self.square_name_to_index("a1")]

            self.squares[self.square_name_to_index("c1")] = king
            self.squares[self.square_name_to_index("d1")] = rook
            self.squares[self.square_name_to_index("c1")].has_moved = True
            self.squares[self.square_name_to_index("d1")].has_moved = True
            self.squares[self.square_name_to_index("e1")] = None
            self.squares[self.square_name_to_index("a1")] = None
            self.castle_right.replace(type, "")
        elif type == "k" and type in self.castle_right:
            king = self.squares[self.square_name_to_index("e8")]
            rook = self.squares[self.square_name_to_index("h8")]

            self.squares[self.square_name_to_index("g8")] = king
            self.squares[self.square_name_to_index("f8")] = rook
            self.squares[self.square_name_to_index("g8")].has_moved = True
            self.squares[self.square_name_to_index("f8")].has_moved = True
            self.squares[self.square_name_to_index("e8")] = None
            self.squares[self.square_name_to_index("h8")] = None
            self.castle_right = self.castle_right = self.castle_right.replace(type, "")
        elif type == "q" and type in self.castle_right:
            king = self.squares[self.square_name_to_index("e8")]
            rook = self.squares[self.square_name_to_index("a8")]

            self.squares[self.square_name_to_index("c8")] = king
            self.squares[self.square_name_to_index("d8")] = rook
            self.squares[self.square_name_to_index("c8")].has_moved = True
            self.squares[self.square_name_to_index("d8")].has_moved = True
            self.squares[self.square_name_to_index("e8")] = None
            self.squares[self.square_name_to_index("a8")] = None
            self.castle_right = self.castle_right.replace(type, "")

    def create_board(self, fen):
        """
        create_board creates board from fen

        Args:
            fen (str): fen string with board position
        """
        self.draw_board()
        self.squares = self.loadPositionFromFenString(fen)
        self.draw_figures_on_board()
        
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

    def draw_figures_on_board(self) -> None:
        """
        Draw all the figures on the chessboard and update the display.
        """
        for idx, figure in enumerate(self.squares):
            # Skip empty squares
            if figure is None:
                continue

            # Calculate the file (column) and rank (row) for the current index
            file = idx % 8
            rank = idx // 8

            # Calculate the x and y coordinates for the figure on the board
            coord_x = file * SQUARE_SIZE
            coord_y = rank * SQUARE_SIZE

            # Draw the figure at the calculated coordinates
            self.draw_figure(coord_x, coord_y, figure)

        # Update the display
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

        return (None, None, None)

    def draw_drag(self, figure) -> None:
        if figure == None:
            return
        
        pos = pygame.Vector2(pygame.mouse.get_pos())
        self.draw_figure(pos[0]-0.5*SQUARE_SIZE, pos[1]-0.5*SQUARE_SIZE, figure)

    def draw_valid_moves(self, figure) -> None:
        if figure == None:
            return
        for move in figure.moves:
            self.draw_tile("#90ee90", int(move.END_SQUARE/8), move.END_SQUARE%8)

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
                color = 0b1 if symbol.islower() else 0b0
                piece = symbolPieceDic[symbol.lower()](color)
                chessboard_array[rank*8 + file] = piece
                file += 1
                
        self.color_to_move = 0b0 if fen.split(" ")[1] == "w" else 0b1
        self.castle_right = fen.split(" ")[2]
        self.en_passant_square = fen.split(" ")[3]
                
        return chessboard_array
    
    def square_name_to_index(self, square_name: str) -> int:
        if square_name == "-": return None
        return ord(square_name[0])-97 + 64-8*int(square_name[1])
    
    def index_to_square_name(self, index: int) -> str:
        ret = f"{chr(index%8 + 97)}{8-int(index/8)}"
        return ret
    