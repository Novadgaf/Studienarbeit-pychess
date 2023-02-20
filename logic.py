squareOffset = [8, -8, -1, 1, 7, -7, 9, -9]
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

class Move():
    def __init__(self, start, end) -> None:
        self.start_square = start
        self.end_square = end