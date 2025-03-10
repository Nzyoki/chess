class Piece:
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    def is_valid_move(self, board, start_x, start_y, end_x, end_y):
        # Base validation for all pieces
        if not board.is_valid_position(end_x, end_y):
            return False
        
        target_piece = board.get_piece(end_x, end_y)
        if target_piece and target_piece.color == self.color:
            return False
        
        return True

class Pawn(Piece):
    def is_valid_move(self, board, start_x, start_y, end_x, end_y):
        if not super().is_valid_move(board, start_x, start_y, end_x, end_y):
            return False

        direction = 1 if self.color == 'black' else -1
        
        # Normal move forward
        if start_y == end_y and end_x == start_x + direction:
            return board.get_piece(end_x, end_y) is None
            
        # Initial two-square move
        if not self.has_moved and start_y == end_y and end_x == start_x + (2 * direction):
            return (board.get_piece(end_x, end_y) is None and 
                   board.get_piece(start_x + direction, start_y) is None)
                   
        # Capture diagonally
        if end_x == start_x + direction and abs(end_y - start_y) == 1:
            return board.get_piece(end_x, end_y) is not None
            
        return False

class Rook(Piece):
    def is_valid_move(self, board, start_x, start_y, end_x, end_y):
        if not super().is_valid_move(board, start_x, start_y, end_x, end_y):
            return False
            
        if start_x != end_x and start_y != end_y:
            return False
            
        # Check path is clear
        step_x = 0 if start_x == end_x else (end_x - start_x) // abs(end_x - start_x)
        step_y = 0 if start_y == end_y else (end_y - start_y) // abs(end_y - start_y)
        
        current_x, current_y = start_x + step_x, start_y + step_y
        while (current_x, current_y) != (end_x, end_y):
            if board.get_piece(current_x, current_y):
                return False
            current_x += step_x
            current_y += step_y
            
        return True

class Knight(Piece):
    def is_valid_move(self, board, start_x, start_y, end_x, end_y):
        if not super().is_valid_move(board, start_x, start_y, end_x, end_y):
            return False
            
        x_diff = abs(end_x - start_x)
        y_diff = abs(end_y - start_y)
        return (x_diff == 2 and y_diff == 1) or (x_diff == 1 and y_diff == 2)

class Bishop(Piece):
    def is_valid_move(self, board, start_x, start_y, end_x, end_y):
        if not super().is_valid_move(board, start_x, start_y, end_x, end_y):
            return False
            
        if abs(end_x - start_x) != abs(end_y - start_y):
            return False
            
        step_x = (end_x - start_x) // abs(end_x - start_x)
        step_y = (end_y - start_y) // abs(end_y - start_y)
        
        current_x, current_y = start_x + step_x, start_y + step_y
        while (current_x, current_y) != (end_x, end_y):
            if board.get_piece(current_x, current_y):
                return False
            current_x += step_x
            current_y += step_y
            
        return True

class Queen(Piece):
    def is_valid_move(self, board, start_x, start_y, end_x, end_y):
        # Queen combines Rook and Bishop movements
        rook = Rook(self.color)
        bishop = Bishop(self.color)
        return (rook.is_valid_move(board, start_x, start_y, end_x, end_y) or 
                bishop.is_valid_move(board, start_x, start_y, end_x, end_y))

class King(Piece):
    def is_valid_move(self, board, start_x, start_y, end_x, end_y):
        if not super().is_valid_move(board, start_x, start_y, end_x, end_y):
            return False
            
        return abs(end_x - start_x) <= 1 and abs(end_y - start_y) <= 1 