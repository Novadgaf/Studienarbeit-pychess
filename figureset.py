
from figures import *

class Figureset():
    def __init__(self) -> None:
        self.chessboard_array: Figure = [[None for x in range(8)] for y in range(8)] 

        for col in range(8):
            self.chessboard_array[1][col] = Pawn(self.FIGURE_LAYER, "black", 1, col)
            self.chessboard_array[6][col] = Pawn(self.FIGURE_LAYER, "white", 6, col)
        
        self.chessboard_array[0][0] = Rook(self.FIGURE_LAYER, "black", 0, 0)
        self.chessboard_array[0][7] = Rook(self.FIGURE_LAYER, "black", 0, 7)
        self.chessboard_array[7][0] = Rook(self.FIGURE_LAYER, "white", 7, 0)
        self.chessboard_array[7][7] = Rook(self.FIGURE_LAYER, "white", 7, 7)

        self.chessboard_array[0][1] = Knight(self.FIGURE_LAYER, "black", 0, 1)
        self.chessboard_array[0][6] = Knight(self.FIGURE_LAYER, "black", 0, 6)
        self.chessboard_array[7][1] = Knight(self.FIGURE_LAYER, "white", 7, 1)
        self.chessboard_array[7][6] = Knight(self.FIGURE_LAYER, "white", 7, 6)

        self.chessboard_array[0][2] = Bishop(self.FIGURE_LAYER, "black", 0, 2)
        self.chessboard_array[0][5] = Bishop(self.FIGURE_LAYER, "black", 0, 5)
        self.chessboard_array[7][2] = Bishop(self.FIGURE_LAYER, "white", 7, 2)
        self.chessboard_array[7][5] = Bishop(self.FIGURE_LAYER, "white", 7, 5)

        self.chessboard_array[0][3] = Queen(self.FIGURE_LAYER, "black", 0, 3)
        self.chessboard_array[7][3] = Queen(self.FIGURE_LAYER, "white", 7, 3)

        self.chessboard_array[0][4] = King(self.FIGURE_LAYER, "black", 0, 4)
        self.chessboard_array[7][4] = King(self.FIGURE_LAYER, "white", 7, 4)