from numpy import empty
import pygame
from constants import *
from chessboard import *
from moveGenerator import MoveGenerator
from move import Move
from tkinter import messagebox
from chessCam import ChessCam


class Pychess():
    def __init__(self) -> None:
        self.main()

    def main(self):
        self.setup_pygame()
        selected_fig = None
        
        
        while True:
            pos_x, pos_y, fig = self.chessboard.get_square_under_mouse()
            moves: list[Move] = self.moveGenerator.generateMoves()
            
            if self.chessboard.color_to_move == self.player_color:
                camMove = self.chessCam.capture_images()
                print(camMove)
                if len(camMove) < 2:
                    continue
                playyerMoves = [self.chessboard.square_name_to_index(x) for x in camMove]
                playerMove = None
                print(moves)
                for figure in moves:
                    print(f"\n\n\n figure in moves {moves} \n\n\n")
                    for validMove in figure:
                        if playyerMoves[0] == validMove.START_SQUARE and playyerMoves[1] == validMove.END_SQUARE:
                            self.chessboard.make_move(validMove)
                        elif playyerMoves[0] == validMove.END_SQUARE and playyerMoves[1] == validMove.START_SQUARE:
                            self.chessboard.make_move(validMove)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if fig == None:
                        continue
                    if fig.COLOR != self.chessboard.color_to_move:
                        continue
                    
                    old_x, old_y, selected_fig = pos_x, pos_y, self.chessboard.squares[pos_y*8 + pos_x]
                    self.chessboard.draw_valid_moves(selected_fig)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.chessboard.draw_board()
                    if selected_fig == None:
                        continue
                    moves = self.moveGenerator.try_move(Move(selected_fig, (old_y*8 + old_x), (pos_y*8 + pos_x)), selected_fig)
                    if moves:
                        self.chessboard.make_move(moves)
                        selected_fig = None
                    else:
                        selected_fig = None

            
            self.FIGURE_LAYER.fill(pygame.Color(0,0,0,0))
            self.chessboard.draw_figures()
            self.chessboard.draw_drag(selected_fig)
            self.WIN.fill("#000000")
            self.WIN.blit(self.BOARD_LAYER,(0,0))
            self.WIN.blit(self.FIGURE_LAYER,(0,0))
            pygame.display.update()

            if not moves:
                messagebox.showinfo("CHECKMATE")


    def setup_pygame(self):
        """
        setup_pygame creates the main window aswell as the layers for the chessboard and figures
        """
        self.player_color = 0b0
        self.chessCam = ChessCam(self.player_color)
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.BOARD_LAYER = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.FIGURE_LAYER = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

        self.chessboard = Chessboard(self.BOARD_LAYER, self.FIGURE_LAYER)
        self.moveGenerator = MoveGenerator(self.chessboard)

    def update_win(self):
        """
        update_win updates the content
        """
        self.WIN.fill("#000000")
        self.WIN.blit(self.BOARD_LAYER,(0,0))
        self.WIN.blit(self.FIGURE_LAYER,(0,0))
        
        pygame.display.update()