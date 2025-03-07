class Piece:
    def __init__(self, color, image_name):
        self.color = color
        self.image_name=f'{color}_{image_name}.png'

class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, 'pawn')

class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, 'rook')

class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, 'knight')


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, 'bishop')

class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, 'queen')

class King(Piece):
    def __init__(self, color):
        super().__init__(color, 'king')
