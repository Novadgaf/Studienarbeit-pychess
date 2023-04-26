class Move():
    def __init__(self, figure, start, end, capture=None, castle = "-", en_passant_square="-") -> None:
        self.FIGURE = figure
        self.START_SQUARE = start
        self.END_SQUARE = end
        self.CAPTURE = capture
        self.EN_PASSANT_SQUARE = en_passant_square
        self.IS_CASTLE = False
        if castle != "-":
            castle(castle)

    def castle(self, type):
        self.IS_CASTLE  = True
        if type == "K":
            self.KING_ENDSQUARE = "g1"
            self.ROOK_ENDSQUARE = "f1"
            pass
        elif type == "Q":
            self.KING_ENDSQUARE = "c1"
            self.ROOK_ENDSQUARE = "d1"
        elif type == "k":
            self.KING_ENDSQUARE = "g8"
            self.ROOK_ENDSQUARE = "f8"
        elif type == "q":
            self.KING_ENDSQUARE = "c8"
            self.ROOK_ENDSQUARE = "d8"
        else:
            self.IS_CASTLE = False
            pass
