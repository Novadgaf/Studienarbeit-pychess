class Figure():
    def __init__(
        self, 
        surface: pygame.Surface, 
        color: str, 
        cord_y: int = 0, 
        cord_x: int = 0,
        ) -> None:
        
        self.SURFACE = surface
        self.COLOR = color

        self.cord_y = cord_y
        self.cord_x = cord_x

class Pawn(Figure):
    """Class for the pawn figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self) -> None:
        super().__init__()
        self.image_path = fr"images/{color}_pawn.png"

class Rook(Figure):
    """Class for the rook figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self) -> None:
        super().__init__()
        self.image_path = fr"images/{color}_rook.png"

        self.has_moved = False

class Knight(Figure):
    """Class for the knight figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self) -> None:
        super().__init__()
        self.image_path = fr"images/{color}_knight.png"

class Bishop(Figure):
    """Class for the bishop figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self) -> None:
        super().__init__()
        self.image_path = fr"images/{color}_bishop.png"

class Queen(Figure):
    """Class for the queen figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self) -> None:
        super().__init__()
        self.image_path = fr"images/{color}_queen.png"

class King(Figure):
    """Class for the king figure

    :param Figure: superclass for this figure
    :type Figure: Figure
    """
    def __init__(self) -> None:
        super().__init__()
        self.image_path = fr"images/{color}_king.png"

        self.has_moved = False
        self.is_checked = False

