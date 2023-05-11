from numpy import empty
import pygame
import pygame.locals as pl
from constants import *
from chessboard import *
from moveGenerator import MoveGenerator
from move import Move
from tkinter import messagebox
from chessCam import ChessCam
from chessboard import square_name_to_index, index_to_square_name
import pygame_gui
from computer import Computer
import matplotlib.pyplot as plt
import numpy as np
import io
import cv2


class Pychess():
    def __init__(self) -> None:
        self.main()

    def main(self):
        self.setup_pygame()
        selected_fig = None
        self.manual_input_state = False
        
        
        # Add the following lines to create the manager, text, button, and slider
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.last_move = "f"
        self.text_label_last_move = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH - 320, 20), (150, 40)),
            text="last move",
            manager=self.manager
        )
        self.text_variable_last_move = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((WIDTH - 170, 20), (150, 40)),
            text="e4,e6",
            manager=self.manager
        )
        self.undo_move_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 310, 60), (150, 40)),
            text="Undo Move",
            manager=self.manager
        )
        self.manual_input_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 160, 60), (150, 40)),
            text="Video input",
            manager=self.manager
        )
        self.capture_board = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((WIDTH - 250, 330), (180, 40)),
            text="Capture position",
            manager=self.manager
        )
        positions = []
        while True:
            time_delta = self.clock.tick(60) / 1000.0
            self.manager.update(time_delta)
            pos_x, pos_y, fig = self.chessboard.get_square_under_mouse()
            moves: list[Move] = self.moveGenerator.generateMoves()
            
            if not moves:
                return
            
            if False:
                if self.chessboard.color_to_move == self.player_color and not self.manual_input_state and len(positions) == 2:
                    camMove = self.chessCam.get_move(positions[0], positions[1])
                    if len(camMove) == 2:
                        playerMoves = [square_name_to_index(x) for x in camMove]
                        if not self.try_user_move(moves, playerMoves): 
                            self.switch_input_type()

                    elif len(camMove) == 4:
                        playerMoves = [square_name_to_index(x) for x in camMove if x[0] in "ceg"]
                        if not self.try_user_move(moves, playerMoves): self.switch_input_type()
                    else:
                        self.switch_input_type()
                    continue
                elif len(positions) > 2:
                    positions = []
                
            for event in pygame.event.get():
                self.manager.process_events(event)
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.undo_move_button:
                            self.chessboard.undo_move()
                        
                        if event.ui_element == self.manual_input_button:
                            self.switch_input_type()

                        if event.ui_element == self.capture_board:
                            positions.append(self.chessCam.capture_image())


                if self.chessboard.color_to_move == self.player_color and self.manual_input_state:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if fig == None:
                            continue
                        if fig.COLOR != self.chessboard.color_to_move:
                            continue
                        
                        old_x, old_y, selected_fig = pos_x, pos_y, self.chessboard.squares[pos_y*8 + pos_x]
                        self.chessboard.draw_valid_moves(selected_fig)
                    if event.type == pygame.MOUSEBUTTONUP:
                        if pos_x == None:
                            selected_fig = None
                            continue
                        self.chessboard.draw_board()
                        if selected_fig == None:
                            continue
                        move = self.moveGenerator.try_move(Move(selected_fig, (old_y*8 + old_x), (pos_y*8 + pos_x)), selected_fig)
                        if move:
                            self.chessboard.make_move(move)
                            self.text_variable_last_move.set_text(f'{index_to_square_name(move.START_SQUARE)},{index_to_square_name(move.END_SQUARE)}')
                        selected_fig = None
                elif self.chessboard.color_to_move != self.player_color:
                    computer_move = self.computer.choose_computer_move()
                    self.chessboard.make_move(computer_move)
                    positions = []

            #live_image = self.chessCam.capture_image()
            #self.plot_surface = self.cv2_image_to_pygame_surface(live_image, 200, 200)
            self.FIGURE_LAYER.fill(pygame.Color(0,0,0,0))
            self.chessboard.draw_figures_on_board()
            self.chessboard.draw_drag(selected_fig)
            self.WIN.fill("#000000")
            self.WIN.blit(self.BOARD_LAYER,(0,0))
            self.WIN.blit(self.FIGURE_LAYER,(0,0))
            #self.WIN.blit(self.plot_surface, (WIDTH - 260, 125))
            self.manager.draw_ui(self.WIN)
            pygame.display.update()

    def setup_pygame(self):
        """
        setup_pygame creates the main window aswell as the layers for the chessboard and figures
        """
        pygame.init()  # Make sure you have this line before initializing the font system
        pygame.font.init()
        self.player_color = 0b0
        #self.chessCam = ChessCam(self.player_color)
        self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.BOARD_LAYER = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.FIGURE_LAYER = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)

        self.chessboard = Chessboard(self.BOARD_LAYER, self.FIGURE_LAYER)
        self.computer = Computer(self.chessboard, 0b1)
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
        for move in aviableMoves:
            if playerMoves[0] == move.START_SQUARE and playerMoves[1] == move.END_SQUARE:
                self.chessboard.make_move(move)
                return True
            elif playerMoves[0] == move.END_SQUARE and playerMoves[1] == move.START_SQUARE:
                self.chessboard.make_move(move)
                return True
        return False
    
    def switch_input_type(self):
        self.manual_input_state = not self.manual_input_state
        if self.manual_input_state:
            self.manual_input_button.set_text("Manual input")
        else:
            self.manual_input_button.set_text("Video input")

    def cv2_image_to_pygame_surface(self, cv2_image, width, height):
        # Resize the image
        resized_image = cv2.resize(cv2_image, (width, height), interpolation=cv2.INTER_AREA)

        # Convert the image from BGR to RGB format
        rgb_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # Create a Pygame surface from the NumPy array
        pygame_surface = pygame.surfarray.make_surface(rgb_image)

        return pygame_surface