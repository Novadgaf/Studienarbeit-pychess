from move import Move


class Figure():
    def __init__(
        self, 
        color, 

        ) -> None:
        self.COLOR = color
        self.NAME = None
        self.TYPE = None
        self.HAS_RANGE_MOVEMENT = False
        self.has_moved = False

        self.moves: list[Move] = []
        

class Pawn(Figure):
    """Class for the pawn figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_pawn.png"
        self.TYPE = "p"


class Rook(Figure):
    """Class for the rook figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_rook.png"
        self.TYPE = "r"
        self.HAS_RANGE_MOVEMENT = True

class Knight(Figure):
    """Class for the knight figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_knight.png"
        self.TYPE = "n"

class Bishop(Figure):
    """Class for the bishop figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.HAS_RANGE_MOVEMENT = True
        self.NAME = fr"{color}_bishop.png"
        self.TYPE = "b"

class Queen(Figure):
    """Class for the queen figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.HAS_RANGE_MOVEMENT = True
        self.NAME = fr"{color}_queen.png"
        self.TYPE = "q"

class King(Figure):
    """Class for the king figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_king.png"
        self.TYPE = "k"

        self.is_checked = False

