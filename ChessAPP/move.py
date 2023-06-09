class Move():
    def __init__(self, figure, start, end, capture=None, castle = "-", en_passant_square="-", is_promotion = False) -> None:
        self.FIGURE = figure
        self.START_SQUARE = start
        self.END_SQUARE = end
        self.CAPTURE = capture
        self.EN_PASSANT_SQUARE = en_passant_square
        self.IS_CASTLE = False
        self.CASTLE_TYPE = castle
        if castle != "-":
            self.IS_CASTLE = True
        self.IS_PROMOTION = is_promotion

    def set_promotion_piece(self, piece):
        self.PROMOTION_PIECE = piece