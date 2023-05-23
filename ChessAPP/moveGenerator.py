from move import Move
from chessboard import square_name_to_index, index_to_square_name
import numpy as np


def calculateSquaresToBorderArray():
        offsets = []
        for idx in range(64):

            file = idx % 8
            rank = int(idx/8)

            north = rank
            south = 7 - rank
            west = file
            east = 7 - file

            offsets.append([
                north, south, west, east, 
                min(north, west), min(south, east), min(north, east), min(south, west)
                ])
        
        return offsets

SQUAREOFFSET = [-8, 8, -1, 1, -9, 9, -7, 7]

#NW, NE, SW, SE, WN, WS, EN, ES
SQUAREOFFSET_KNIGHT = [-17, -15, 15, 17, -10, 6, -6, 10]

BORDER_OFFSETS = calculateSquaresToBorderArray()

class MoveGenerator:

    def __init__(self, chessboard) -> None:
        self.chessboard = chessboard          

    def generateMoves(self, color=None, figures = "rnbqkp"):
        """generates all possible moves for every figure on the board

        :return: list of possible moves
        :rtype: list[Move]
        """
        if color == None:
            color = self.chessboard.color_to_move

        player_moves = []
        for idx, figure in enumerate(self.chessboard.squares):
            if figure == None: continue
            if figure.COLOR != color: continue

            if figure.HAS_RANGE_MOVEMENT and figure.TYPE in figures: 
                figure.moves = self.generateRangeMoves(idx)

            elif figure.TYPE == "k" and figure.TYPE in figures:
                figure.moves = self.generateKingMoves(idx)

            elif figure.TYPE == "p" and figure.TYPE in figures:
                figure.moves = self.generatePawnMoves(idx)

            elif figure.TYPE == "n" and figure.TYPE in figures:
                figure.moves = self.generateKnightMoves(idx)
            else:
                figure.moves = []

            if figure.moves: player_moves.append(figure.moves)
        tmp =[move for sublist in player_moves for move in sublist]
        return tmp

    def generateRangeMoves(self, start_square: int) -> list[Move]:
        """generate all possible moves for a range movement figure on the board

        :param figure: figure to generate the moves for
        :type figure: Figure
        :param square_id: square id in the array
        :type square_id: int
        :return: list of moves for the figure
        :rtype: list[Move]
        """
        border_offsets = BORDER_OFFSETS[start_square]
        figure = self.chessboard.squares[start_square]


        figure_border_offets = []
        figure_square_offsets = []
        moves = []


        if figure.TYPE != "b":
            figure_border_offets.append(border_offsets[:4])
            figure_square_offsets.append(SQUAREOFFSET[:4])
        
        if figure.TYPE != "r":
            figure_border_offets.append(border_offsets[4:])
            figure_square_offsets.append(SQUAREOFFSET[4:])

        figure_border_offets = [item for sublist in figure_border_offets for item in sublist]
        figure_square_offsets = [item for sublist in figure_square_offsets for item in sublist]
        for border_offset, square_offset in zip(figure_border_offets, figure_square_offsets):
            for x in range(1, border_offset+1):

                end_square = start_square + x*square_offset
                move = Move(figure, start_square, end_square)

                if self.chessboard.squares[end_square] == None:
                    if self.check_valid_move(move): moves.append(move)
                    
                elif self.chessboard.squares[end_square].COLOR != self.chessboard.color_to_move:
                    move.CAPTURE = end_square
                    if self.check_valid_move(move): moves.append(move)
                    break
                
                else:
                    break
        return moves


    def generateKingMoves(self, start_square: int) -> list[Move]:
        borderOffsets = BORDER_OFFSETS[start_square]
        figure = self.chessboard.squares[start_square]

        moves = []

        for border_offset, square_offset in zip(borderOffsets, SQUAREOFFSET):
            if border_offset > 0:
                end_square = start_square + square_offset
                move = Move(figure, start_square, end_square)

                if self.chessboard.squares[end_square] == None:
                    if self.check_valid_move(move): moves.append(move)

                elif self.chessboard.squares[end_square].COLOR != self.chessboard.color_to_move:
                    move.CAPTURE = end_square
                    if self.check_valid_move(move): moves.append(move)
        
        moves.extend(self.getCastleMoves())

        return moves   
    
    def getCastleMoves(self) -> list:
        king_square = self.find_king_square(self.chessboard.squares)
        king_figure = self.chessboard.squares[king_square]
        moves = []
        if king_figure.has_moved or self.check_for_checks(self.chessboard.squares)>0:
            return moves


        if king_figure.COLOR == 0b0:
            queenside_rook = self.chessboard.squares[56]
            kingside_rook = self.chessboard.squares[63]
        else:
            queenside_rook = self.chessboard.squares[0]
            kingside_rook = self.chessboard.squares[7]
        
        if queenside_rook != None:
            if not queenside_rook.has_moved:
                if self.chessboard.squares[king_square-1] == None and self.chessboard.squares[king_square-2] == None:
                    move1 = Move(king_figure, king_square, king_square-1)
                    move2 = Move(king_figure, king_square, king_square-2)

                    if self.check_valid_move(move1) and self.check_valid_move(move2):
                        castle_type = "Q" if king_figure.COLOR == 0b0 else "q"
                        moves.append(Move(king_figure, king_square, king_square-2, castle=castle_type))
        
        if kingside_rook != None:
            if not kingside_rook.has_moved:
                if self.chessboard.squares[king_square+1] == None and self.chessboard.squares[king_square+2] == None:
                    move1 = Move(king_figure, king_square, king_square+1)
                    move2 = Move(king_figure, king_square, king_square+2)

                    if self.check_valid_move(move1) and self.check_valid_move(move2):
                        castle_type = "K" if king_figure.COLOR == 0b0 else "k"
                        moves.append(Move(king_figure, king_square, king_square+2, castle=castle_type))

        return moves

        
        

    def generateKnightOffsets(self, figure_square) -> list:
        border_offset = BORDER_OFFSETS[figure_square]
        figure_offsets = SQUAREOFFSET_KNIGHT.copy()

        if border_offset[0] < 2:
            figure_offsets[0] = 0
            figure_offsets[1] = 0
            if border_offset[0] == 0:
                figure_offsets[4] = 0
                figure_offsets[6] = 0

        if border_offset[1] < 2:
            figure_offsets[2] = 0
            figure_offsets[3] = 0
            if border_offset[1] == 0:
                figure_offsets[5] = 0
                figure_offsets[7] = 0

        if border_offset[2] < 2: 
            figure_offsets[4] = 0
            figure_offsets[5] = 0
            if border_offset[2] == 0:
                figure_offsets[0] = 0
                figure_offsets[2] = 0

        if border_offset[3] < 2:
            figure_offsets[6] = 0
            figure_offsets[7] = 0
            if border_offset[3] == 0:
                figure_offsets[1] = 0
                figure_offsets[3] = 0

        return figure_offsets

    def generateKnightMoves(self, start_square: int) -> list[Move]:
        figure_offsets = self.generateKnightOffsets(start_square)
        figure = self.chessboard.squares[start_square]
        moves = []

        for os in figure_offsets:

            if os == 0: continue

            end_square = start_square+os
            move = Move(figure, start_square, end_square)
            if self.chessboard.squares[end_square] != None:
                if self.chessboard.squares[end_square].COLOR == self.chessboard.color_to_move:
                    continue
                elif self.chessboard.squares[end_square].COLOR != self.chessboard.color_to_move: 
                    move.CAPTURE = end_square
            if self.check_valid_move(move): moves.append(move)
        
        return moves


    def generatePawnMoves(self, start_square: int) -> list[Move]:
        figure = self.chessboard.squares[start_square]

        walking_direction = 1 if figure.COLOR == 0b0 else -1

        moves = []
        end_square = start_square+SQUAREOFFSET[0]*walking_direction

        if self.chessboard.squares[end_square] == None:
            move = Move(figure, start_square, end_square)
            if self.check_valid_move(move): moves.append(move)

            rank = int(start_square/8)
            if figure.COLOR == 0b0 and rank == 6 or figure.COLOR == 0b1 and rank == 1:
                end_square = start_square+2*SQUAREOFFSET[0]*walking_direction
                
                if self.chessboard.squares[end_square] == None:
                    ep_square = end_square+SQUAREOFFSET[0]*(-1)*walking_direction
                    move = Move(figure, start_square, end_square, en_passant_square=index_to_square_name(ep_square))
                    if self.check_valid_move(move): moves.append(move)

        #pawn capture
        end_square = start_square+SQUAREOFFSET[4]*walking_direction
        if self.chessboard.squares[end_square] != None  and abs(start_square%8 - end_square%8) == 1 and abs(int(start_square/8) - int(end_square/8)) == 1:
            if  self.chessboard.squares[end_square].COLOR != figure.COLOR:
                move = Move(figure, start_square, end_square, capture=end_square)
                if self.check_valid_move(move): moves.append(move)
        
        end_square = start_square+SQUAREOFFSET[6]*walking_direction
        if self.chessboard.squares[end_square] != None and abs(start_square%8 - end_square%8) == 1 and abs(int(start_square/8) - int(end_square/8)) == 1:
            if  self.chessboard.squares[end_square].COLOR != figure.COLOR:
                move = Move(figure, start_square, end_square, capture=end_square)
                if self.check_valid_move(move): moves.append(move)

        #En passant
        end_square = square_name_to_index(self.chessboard.en_passant_square)
        if end_square != None:
            if abs(start_square%8 - end_square%8) == 1 and abs(int(start_square/8) - int(end_square/8)) == 1:
                move = Move(figure, start_square, end_square, capture=end_square+(8)*walking_direction)
                if self.check_valid_move(move): moves.append(move)

        return moves

    def try_move(self, move: Move, figure):
        for valid_move in figure.moves:
            if valid_move.START_SQUARE == move.START_SQUARE and valid_move.END_SQUARE == move.END_SQUARE:
                return valid_move
        return None
    
    def find_king_square(self, position, color=None) -> int:
        if color==None:
            color = self.chessboard.color_to_move
        for idx, figure in enumerate(position):
            if figure == None: continue
            if figure.COLOR != color: continue
            if figure.TYPE == "k": return idx


    def check_for_checks(self, position: list) -> int:
        checks = 0
        king_square = self.find_king_square(position)
        if not king_square: 
            return 666
        king_figure = position[king_square]

        figure_border_offets = BORDER_OFFSETS[king_square]

        #find rook / queen checks
        figure_square_offsets = SQUAREOFFSET[:4]

        for border_offset, square_offset in zip(figure_border_offets[:4], figure_square_offsets):
            for x in range(1, border_offset+1):
                end_square = king_square + x*square_offset

                end_square_figure = position[end_square]

                if end_square_figure == None:
                    continue

                elif end_square_figure.COLOR != self.chessboard.color_to_move:
                    if end_square_figure.TYPE == "r" or end_square_figure.TYPE == "q":
                        checks += 1
                    else: 
                        break
                else:
                    break

        #find bishop / queen checks
        figure_square_offsets = SQUAREOFFSET[4:]
        for border_offset, square_offset in zip(figure_border_offets[4:], figure_square_offsets):
            for x in range(1, border_offset+1):
                end_square = king_square + x*square_offset

                end_square_figure = position[end_square]

                if end_square_figure == None:
                    continue

                elif end_square_figure.COLOR != self.chessboard.color_to_move:
                    if end_square_figure.TYPE == "b" or end_square_figure.TYPE == "q":
                        checks += 1
                    else:
                        break

                else:
                    break

        #find knight checks
        figure_offsets = self.generateKnightOffsets(king_square)

        for os in figure_offsets:
            if os == 0: continue

            end_square_figure = position[king_square+os]
            if end_square_figure != None:
                if end_square_figure.COLOR != king_figure.COLOR and end_square_figure.TYPE == "n":
                    checks += 1

        #find pawn checks
        walking_direction = 1 if king_figure.COLOR == 0b0 else -1
        end_square = king_square+SQUAREOFFSET[4]*walking_direction
        if position[end_square] != None:
            if  position[end_square].COLOR != king_figure.COLOR and position[end_square].TYPE == "p":
                checks += 1
        
        end_square = king_square+SQUAREOFFSET[6]*walking_direction
        if position[end_square] != None:
            if  position[end_square].COLOR != king_figure.COLOR and position[end_square].TYPE == "p":
                checks += 1

        #find king attacks
        for border_offset, square_offset in zip(figure_border_offets, SQUAREOFFSET):
            if border_offset == 0: 
                continue

            end_square = king_square + square_offset
            end_square_figure = position[end_square]

            if end_square_figure == None:
                    continue
            elif end_square_figure.COLOR != king_figure.COLOR:
                if end_square_figure.TYPE == "k":
                    checks += 1

        return checks
    
    def check_valid_move(self, move: Move) -> bool:

        new_position = self.chessboard.squares.copy()
        new_position[move.START_SQUARE] = None
        new_position[move.END_SQUARE] = move.FIGURE
        if self.check_for_checks(new_position) == 0: return True
            
        else: return False

    def get_attacked_squares(self, color, figures = "rnbqkp"):
        moves = self.generateMoves(color, figures)
        attacked_squares = []
        for move in moves:
            attacked_squares.append(move.END_SQUARE)
        return attacked_squares