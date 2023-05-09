from numpy import empty
import pygame
import pygame.locals as pl
from constants import *
from chessboard import *
from moveGenerator import MoveGenerator
from move import Move
from tkinter import messagebox
from chessCam import ChessCam
import pygame_gui


class Pychess():
    def __init__(self) -> None:
        self.main()

    def main(self):
        self.setup_pygame()
        selected_fig = None
        skip_camera_move = False
        
        # Add the following lines to create the manager, text, button, and slider
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.text_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH - 320, 20), (300, 40)),
            text="Some text here",
            manager=self.manager
        )
        self.undo_move_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 320, 70), (100, 40)),
            text="Undo Move",
            manager=self.manager
        )
        self.manual_input_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((WIDTH - 320, 130), (100, 20)),
            start_value=0,
            value_range=(0, 1),
            manager=self.manager
        )
        self.manual_input_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH - 210, 125), (100, 40)),
            text="Manual Input",
            manager=self.manager
        )
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            self.manager.update(time_delta)
            pos_x, pos_y, fig = self.chessboard.get_square_under_mouse()
            moves: list[Move] = self.moveGenerator.generateMoves()
            if not moves:
                return

            if self.chessboard.color_to_move == self.player_color and not skip_camera_move:
                camMove = self.chessCam.capture_images()
                if len(camMove) == 2:
                    playerMoves = [self.chessboard.square_name_to_index(x) for x in camMove]
                    if not self.try_user_move(moves, playerMoves): skip_camera_move = True

                elif len(camMove) == 4:
                    playerMoves = [self.chessboard.square_name_to_index(x) for x in camMove if x[0] in "ceg"]
                    if not self.try_user_move(moves, playerMoves): skip_camera_move = True
                else:
                    skip_camera_move = True

                

            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.undo_move_button:
                            print("pressed")

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
                    move = self.moveGenerator.try_move(Move(selected_fig, (old_y*8 + old_x), (pos_y*8 + pos_x)), selected_fig)
                    if move:
                        self.chessboard.make_move(move)
                        skip_camera_move = False
                    selected_fig = None

            
            self.FIGURE_LAYER.fill(pygame.Color(0,0,0,0))
            self.chessboard.draw_figures()
            self.chessboard.draw_drag(selected_fig)
            self.WIN.fill("#000000")
            self.WIN.blit(self.BOARD_LAYER,(0,0))
            self.WIN.blit(self.FIGURE_LAYER,(0,0))
            self.manager.draw_ui(self.WIN)
            pygame.display.update()

    def setup_pygame(self):
        """
        setup_pygame creates the main window aswell as the layers for the chessboard and figures
        """
        pygame.init()  # Make sure you have this line before initializing the font system
        pygame.font.init()
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

    def try_user_move(self, aviableMoves, playerMoves):
        for figure in aviableMoves:
                    for validMove in figure:
                        if playerMoves[0] == validMove.START_SQUARE and playerMoves[1] == validMove.END_SQUARE:
                            self.chessboard.make_move(validMove)
                            return False
                        elif playerMoves[0] == validMove.END_SQUARE and playerMoves[1] == validMove.START_SQUARE:
                            self.chessboard.make_move(validMove)
                            return False
        return True