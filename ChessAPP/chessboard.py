from typing import Tuple, List, Optional, Dict, NamedTuple, Union
from constants import *
import pygame
from figures import *
import os
import copy


class SquareInfo(NamedTuple):
    x: Union[int, None]
    y: Union[int, None]
    piece: Union[Figure, None]

#NW, NE, SW, SE, WN, WS, EN, ES
SQUAREOFFSET_KNIGHT = [-17, -15, 15, 17, -10, 6, -6, 10]

class Chessboard:
    def __init__(self, board_surface: pygame.Surface, figure_surface: pygame.Surface, fen: str = STARTFEN) -> None:
        self.BOARD_SURFACE = board_surface
        self.FIGURE_SURFACE = figure_surface
        self.IMAGES = self.load_figure_images()
        self.color_to_move = 0b0
        self.castle_right = "KQkq"
        self.en_passant_square = "-"
        self.pieces_affected_by_move = []
        self.saved_state = None
        self.create_board(fen)


    def save_state(self) -> None:
        """
        saves the current state of the game
        """
        state = {
            'color_to_move': self.color_to_move,
            'castle_right': self.castle_right,
            'en_passant_square': self.en_passant_square,
            'squares': copy.deepcopy(self.squares),
            'saved_state': copy.deepcopy(self.saved_state)
        }
        self.saved_state = state


    def restore_state(self) -> None:
        """
        loads the game from its previous version
        """
        if self.saved_state:
            self.color_to_move = self.saved_state['color_to_move']
            self.castle_right = self.saved_state['castle_right']
            self.en_passant_square = self.saved_state['en_passant_square']
            self.squares = self.saved_state['squares']
            self.saved_state = self.saved_state['saved_state']
        else:
            print("No saved state available.")


    def undo_move(self) -> None:
        """
        undos the last move and restores the version before the previous version of the game
        """
        self.restore_state()
        self.restore_state()


    def make_move(self, move: Move) -> None:
        self.save_state()
        self.color_to_move = self.color_to_move ^ 0b1
        self.en_passant_square = move.EN_PASSANT_SQUARE

        if move.IS_CASTLE:
            self.castle(move.CASTLE_TYPE)
            return

        if move.CAPTURE is not None:
            self.squares[move.CAPTURE] = None
        self.squares[move.START_SQUARE] = None
        self.squares[move.END_SQUARE] = move.FIGURE
        self.squares[move.END_SQUARE].has_moved = True


    def update_affected_pieces(move: Move):
        affected_pieces = [move.END_SQUARE]
        for x in SQUAREOFFSET_KNIGHT:
            affected_pieces.append(move.END_SQUARE+SQUAREOFFSET_KNIGHT)
            affected_pieces.append(move.START_SQUARE+SQUAREOFFSET_KNIGHT)



    def _move_castle_pieces(self, king_src: str, king_dst: str, rook_src: str, rook_dst: str) -> None:
        """
        Helper function to move the king and rook during castling.

        Args:
            king_src (str): The source square of the king.
            king_dst (str): The destination square of the king.
            rook_src (str): The source square of the rook.
            rook_dst (str): The destination square of the rook.
        """
        king = self.squares[square_name_to_index(king_src)]
        rook = self.squares[square_name_to_index(rook_src)]

        self.squares[square_name_to_index(king_dst)] = king
        self.squares[square_name_to_index(rook_dst)] = rook
        self.squares[square_name_to_index(king_dst)].has_moved = True
        self.squares[square_name_to_index(rook_dst)].has_moved = True
        self.squares[square_name_to_index(king_src)] = None
        self.squares[square_name_to_index(rook_src)] = None
        

    def castle(self, type: str) -> None:
        """
        castle updates the board position for the given castling type.

        Args:
            type (str): the type of castling ("K", "Q", "k", or "q")
        """
        if type not in self.castle_right:
            return

        castling_moves = {
            "K": ("e1", "g1", "h1", "f1"),
            "Q": ("e1", "c1", "a1", "d1"),
            "k": ("e8", "g8", "h8", "f8"),
            "q": ("e8", "c8", "a8", "d8"),
        }

        king_src, king_dst, rook_src, rook_dst = castling_moves[type]
        self._move_castle_pieces(king_src, king_dst, rook_src, rook_dst)
        self.castle_right = self.castle_right.replace(type, "")


    def create_board(self, fen: str) -> None:
        """
        create_board creates a board from a FEN string.

        Args:
            fen (str): FEN string with board position
        """
        self.draw_board()
        self.squares = self.loadPositionFromFenString(fen)
        self.draw_figures_on_board()


    def draw_board(self) -> None:
        """
        Draw the chessboard with alternating colors for the squares.
        """

        # Iterate through each square on the chessboard
        for row in range(8):
            for col in range(8):

                # Determine the color of the square based on its position
                color = self._get_square_color(row, col)

                # Draw the square with the determined color
                self.draw_tile(color, col, row)

        # Update the display to show the drawn chessboard
        pygame.display.update()


    def _get_square_color(self, row: int, col: int) -> Tuple[int, int, int]:
        """
        Helper function to get the color of a square on the chessboard.

        Args:
            row (int): The row number of the square (0-7).
            col (int): The column number of the square (0-7).

        Returns:
            Tuple[int, int, int]: The RGB color of the square.
        """
        if (row + col) % 2 != 0:
            return COLOR_BLACK
        else:
            return COLOR_WHITE


    def draw_tile(self, color: str, cord_y: int, cord_x: int) -> None:
        """
        draw_tile draws a single colored rectangle.

        Args:
            color (str): color of the rectangle
            cord_y (int): y-coordinate of the rectangle (0-7)
            cord_x (int): x-coordinate of the rectangle (0-7)
        """
        pygame.draw.rect(self.BOARD_SURFACE, color, [SQUARE_SIZE*cord_x, SQUARE_SIZE*cord_y, SQUARE_SIZE, SQUARE_SIZE])


    def load_figure_images(self) -> Dict[str, pygame.Surface]:
        """
        Load all figure images into a dictionary.

        Returns:
            dict: Dictionary containing an image for each figure.
        """
        images_directory = "./images"
        images = {}

        try:
            filenames = next(os.walk(images_directory), (None, None, []))[2]  # [] if no file
        except StopIteration:
            raise FileNotFoundError(f"No files found in the images directory: {images_directory}")

        for filename in filenames:
            path = os.path.join(images_directory, filename)

            # Load the image, scale it, and add it to the images dictionary
            img = self._load_and_scale_image(path)
            images[filename] = img

        return images


    def _load_and_scale_image(self, path: str) -> pygame.Surface:
        """
        Helper function to load an image and scale it to the desired size.

        Args:
            path (str): Path of the image file to load.

        Returns:
            pygame.Surface: Scaled image surface.
        """
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

        return img


    def draw_figure(self, cord_x: int, cord_y: int, figure: Figure) -> None:
        """
        draw_figure draws a single figure.

        Args:
            cord_x (int): x position to draw
            cord_y (int): y position to draw
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


    def get_square_under_mouse(self) -> SquareInfo:
        """
        Get the x, y position of the mouse and the piece underneath.

        Returns:
            SquareInfo: NamedTuple containing x, y coordinates and the piece under the mouse
        """
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        pos_x, pos_y = [int(v // SQUARE_SIZE) for v in mouse_pos]

        if 0 <= pos_x < 8 and 0 <= pos_y < 8:
            return SquareInfo(x=pos_x, y=pos_y, piece=self.squares[pos_y * 8 + pos_x])

        return SquareInfo(x=None, y=None, piece=None)


    def draw_drag(self, figure: Optional[Figure]) -> None:
        """
        draw_drag draws the figure being dragged by the mouse.

        Args:
            figure (Figure): figure to draw while dragging
        """
        if figure is None:
            return

        # Get the current mouse position as a 2D vector
        mouse_position = pygame.Vector2(pygame.mouse.get_pos())

        # Calculate the drawing position by subtracting half the square size
        draw_position_x = mouse_position[0] - 0.5 * SQUARE_SIZE
        draw_position_y = mouse_position[1] - 0.5 * SQUARE_SIZE

        # Draw the figure at the calculated position
        self.draw_figure(draw_position_x, draw_position_y, figure)


    def draw_valid_moves(self, figure: Optional[Figure]) -> None:
        """
        draw_valid_moves draws the valid moves for the given figure.

        Args:
            figure (Figure): figure for which to draw valid moves
        """
        if figure is None:
            return

        # Iterate through all valid moves for the given figure
        for move in figure.moves:
            # Calculate the rank (row) and file (column) for the end square of the move
            rank = int(move.END_SQUARE / 8)
            file = move.END_SQUARE % 8

            # Draw a tile with a distinct color to indicate a valid move
            self.draw_tile("#90ee90", rank, file)


    def loadPositionFromFenString(self, fen: str) -> List[Optional[Figure]]:
        """
        loadPositionFromFenString loads the position from a FEN string.

        Args:
            fen (str): FEN string with board position

        Returns:
            List[Optional[Figure]]: list of figures on the board
        """
        symbol_to_piece = {
            "p": Pawn,
            "r": Rook,
            "n": Knight,
            "b": Bishop,
            "q": Queen,
            "k": King
        }

        chessboard_squares = [None for _ in range(64)]

        rank = 0
        file = 0

        position_info = fen.split(" ")
        position = position_info[0]

        for symbol in position:
            if symbol == "/":
                file = 0
                rank += 1
                continue

            if symbol.isnumeric():
                file += int(symbol)
            else:
                color = 0b1 if symbol.islower() else 0b0
                piece = symbol_to_piece[symbol.lower()](color)
                chessboard_squares[rank * 8 + file] = piece
                file += 1

        self.color_to_move = 0b0 if position_info[1] == "w" else 0b1
        self.castle_right = position_info[2]
        self.en_passant_square = position_info[3]

        return chessboard_squares


def square_name_to_index(square_name: str) -> Optional[int]:
    """
    square_name_to_index converts square name (e.g., "a1") to an index in the squares list.

    Args:
        square_name (str): square name to convert

    Returns:
        Optional[int]: index in the squares list, or None if invalid input
    """
    if square_name == "-":
        return None

    file_offset = ord(square_name[0]) - ord("a")
    rank_offset = 8 - int(square_name[1])

    return file_offset + 8 * rank_offset


def index_to_square_name(index: int) -> str:
    """
    index_to_square_name converts an index in the squares list to a square name (e.g., "a1").

    Args:
        index (int): index in the squares list to convert

    Returns:
        str: square name corresponding to the index
    """
    file = chr(index % 8 + ord('a'))
    rank = 8 - (index // 8)

    return f"{file}{rank}"