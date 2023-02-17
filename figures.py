
class Figure():
    def __init__(
        self, 
        color: str, 
        ) -> None:
        self.COLOR = color
        self.NAME = None

class Pawn(Figure):
    """Class for the pawn figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_pawn.png"

class Rook(Figure):
    """Class for the rook figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_rook.png"

        self.has_moved = False

class Knight(Figure):
    """Class for the knight figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_knight.png"

class Bishop(Figure):
    """Class for the bishop figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_bishop.png"

class Queen(Figure):
    """Class for the queen figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_queen.png"

class King(Figure):
    """Class for the king figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.NAME = fr"{color}_king.png"

        self.has_moved = False
        self.is_checked = False

