

SQUAREOFFSET = [-8, 8, -1, 1, -9, 9, -7, 7]

#NW, NE, SW, SE, WN, WS, EN, ES
SQUAREOFFSET_KNIGHT = [-17, -15, 15, 17, -10, 6, -6, 10]

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

class Move():
    def __init__(self, start, end) -> None:
        self.START_SQUARE = start
        self.END_SQUARE = end

def generateMoves(chessboard):
    """generates all possible moves for every figure on the board

    :return: list of possible moves
    :rtype: list[Move]
    """

    for idx, figure in enumerate(chessboard.squares):
        if figure == None: continue
        if figure.COLOR != chessboard.color_to_move: continue

        if figure.HAS_RANGE_MOVEMENT: 
            figure.moves = generateRangeMoves(chessboard, idx)

        if figure.TYPE == "k":
            figure.moves = generateKingMoves(chessboard, idx)

        if figure.TYPE == "p":
            figure.moves = generatePawnMoves(chessboard, idx)

        if figure.TYPE == "n":
            figure.moves = generateKnightMoves(chessboard, idx)

def generateRangeMoves(chessboard, start_square: int) -> list[Move]:
    """generate all possible moves for a range movement figure on the board

    :param figure: figure to generate the moves for
    :type figure: Figure
    :param square_id: square id in the array
    :type square_id: int
    :return: list of moves for the figure
    :rtype: list[Move]
    """

    border_offsets = calculateSquaresToBorderArray()
    border_offsets = border_offsets[start_square]
    figure = chessboard.squares[start_square]


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
            move = Move(start_square, end_square)

            if chessboard.squares[end_square] == None:
                moves.append(move)

            elif chessboard.squares[end_square].COLOR != chessboard.color_to_move:
                moves.append(move)
                break
            
            else:
                break
    return moves


def generateKingMoves(chessboard, start_square: int) -> list[Move]:
    borderOffsets = calculateSquaresToBorderArray()
    borderOffsets = borderOffsets[start_square]
    figure = chessboard.squares[start_square]

    moves = []

    for border_offset, square_offset in zip(borderOffsets, SQUAREOFFSET):
        if border_offset > 0:
            end_square = start_square + square_offset
            move = Move(start_square, end_square)

            if chessboard.squares[end_square] == None:
                moves.append(move)

            elif chessboard.squares[end_square].COLOR != chessboard.color_to_move:
                moves.append(move)

    return moves   


def generateKnightMoves(chessboard, start_square: int) -> list[Move]:
    border_offset = calculateSquaresToBorderArray()
    border_offset = border_offset[start_square]
    figure_offsets = SQUAREOFFSET_KNIGHT.copy()
    moves = []

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


    for os in figure_offsets:

        if os == 0: continue

        end_square = start_square+os
        if chessboard.squares[end_square] != None:
            if chessboard.squares[end_square].COLOR == chessboard.color_to_move:
                continue
        
        moves.append(Move(start_square, end_square))
    
    return moves


def generatePawnMoves(chessboard, start_square: int) -> list[Move]:
    borderOffsets = calculateSquaresToBorderArray()
    borderOffsets = borderOffsets[start_square]
    figure = chessboard.squares[start_square]

    walking_direction = 1 if figure.COLOR == 0b0 else -1

    moves = []
    end_square = start_square+SQUAREOFFSET[0]*walking_direction

    if chessboard.squares[end_square] == None:
        moves.append(Move(start_square, end_square))

        rank = int(start_square/8)
        if figure.COLOR == 0b0 and rank == 5 or figure.COLOR == 0b1 and rank == 1:
            end_square = start_square+2*SQUAREOFFSET[0]*walking_direction
            
            if chessboard.squares[end_square] == None:
                moves.append(Move(start_square, end_square))

    end_square = start_square+SQUAREOFFSET[4]*walking_direction
    if chessboard.squares[end_square] != None and abs(start_square%8 - end_square%8) == 1:
        if  chessboard.squares[end_square].COLOR != figure.COLOR:
            moves.append(Move(start_square, end_square))
    
    end_square = start_square+SQUAREOFFSET[6]*walking_direction
    if chessboard.squares[end_square] != None and abs(start_square%8 - end_square%8) == 1:
        if  chessboard.squares[end_square].COLOR != figure.COLOR:
            moves.append(Move(start_square, end_square))

    return moves





def check_valid_move(move: Move, figure):
    for valid_move in figure.moves:
        if valid_move.START_SQUARE == move.START_SQUARE and valid_move.END_SQUARE == move.END_SQUARE:
            return True
    return False