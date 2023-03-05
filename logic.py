

SQUAREOFFSET = [8, -8, -1, 1, 7, -7, 9, -9]
squaresToBorder = [[None for x in range(8)] for y in range(64)]

def calculateSquaresToBorderArray():
    for idx, offsets in enumerate(squaresToBorder):

        file = idx % 8
        rank = int(idx/8)

        north = rank
        south = 7 - rank
        west = file
        east = 7 - file

        offsets = [
            north, south, west, east, 
            min(north, west), min(south, east), min(north, east), min(south, west)
            ]
    
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
    figure = chessboard[start_square]


    figure_border_offets = []
    figure_square_offsets = []
    moves = []


    if figure.TYPE != "b":
        figure_border_offets.append(border_offsets[:4])
        figure_square_offsets.append(SQUAREOFFSET[:4])
    
    if figure.TYPE != "r":
        figure_border_offets.append(border_offsets[4:])
        figure_square_offsets.append(SQUAREOFFSET[4:])

    for border_offset, square_offset in (figure_border_offets, figure_square_offsets):
        for x in range(border_offset):

            end_square = start_square + x*square_offset
            move = Move(start_square, end_square)

            if chessboard[end_square] == None:
                moves.append(move)

            elif chessboard[end_square].COLOR != chessboard.color_to_move:
                moves.append(move)
                break
            
            else:
                break

    return moves

        