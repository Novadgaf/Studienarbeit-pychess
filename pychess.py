from numpy import empty
import pygame
from constants import *
from chessboard import *
import logic
import sys


class Pychess():
    def __init__(self) -> None:
        self.main()

    def main(self):
        self.setup_pygame()

        selected_fig = None
        
        while True:
            pos_x, pos_y, fig = self.chessboard.get_square_under_mouse()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if fig == None:
                        continue
                    if fig.COLOR != self.chessboard.color_to_move:
                        continue
                    logic.generateMoves(self.chessboard)
                    old_x, old_y, selected_fig = pos_x, pos_y, self.chessboard.squares[pos_y*8 + pos_x]
                    self.chessboard.draw_valid_moves(selected_fig)
                    self.chessboard.squares[old_y*8 + old_x] = None
                if event.type == pygame.MOUSEBUTTONUP:
                    self.chessboard.draw_board()
                    if selected_fig == None:
                        if fig == None:
                            continue
                        if fig.COLOR != self.chessboard.color_to_move:
                            continue
                    move = logic.Move((old_y*8 + old_x), (pos_y*8 + pos_x))
                    if logic.check_valid_move(move, selected_fig):
                        self.chessboard.squares[pos_y*8 + pos_x] = selected_fig
                        selected_fig = None
                        self.chessboard.color_to_move = self.chessboard.color_to_move^0b1
                    else:
                        self.chessboard.squares[old_y*8 + old_x] = selected_fig
                        selected_fig = None

            
            self.FIGURE_LAYER.fill(pygame.Color(0,0,0,0))
            self.chessboard.draw_figures()
            self.chessboard.draw_drag(selected_fig)
            self.WIN.fill("#000000")
            self.WIN.blit(self.BOARD_LAYER,(0,0))
            self.WIN.blit(self.FIGURE_LAYER,(0,0))
            pygame.display.update()



    def setup_pygame(self):
        """
        setup_pygame creates the main window aswell as the layers for the chessboard and figures
        """
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.BOARD_LAYER = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.FIGURE_LAYER = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

        self.chessboard = Chessboard(self.BOARD_LAYER, self.FIGURE_LAYER)

    def update_win(self):
        """
        update_win updates the content
        """
        self.WIN.fill("#000000")
        self.WIN.blit(self.BOARD_LAYER,(0,0))
        self.WIN.blit(self.FIGURE_LAYER,(0,0))
        
        pygame.display.update()