class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        

    def place_piece(self, row, col, piece):
        self.board[row][col] = piece

    def move_piece(self, start_x, start_y, end_x, end_y):
        if self.board[start_x][start_y]:
            self.board[end_x][end_y] = self.board[start_x][start_y]
            self.board[start_x][start_y] = None
            return True
        return False
    
    def setup_pieces(self):
        from pieces import Pawn, Rook,Knight, Bishop, Queen, King
        self.place_piece(0, 0, Rook('black'))
        self.place_piece(0, 7, Rook('black'))
        self.place_piece(0, 1, Knight('black'))
        self.place_piece(0, 6, Knight('black')) 
        self.place_piece(0, 2, Bishop('black'))
        self.place_piece(0, 5, Bishop('black'))  
        self.place_piece(0, 3, Queen('black'))
        self.place_piece(0, 4, King('black'))
        
        self.place_piece(7, 0, Rook('white'))
        self.place_piece(7, 7, Rook('white'))
        self.place_piece(7, 1, Knight('white'))
        self.place_piece(7, 6, Knight('white'))
        self.place_piece(7, 2, Bishop('white'))
        self.place_piece(7, 5, Bishop('white'))
        self.place_piece(7, 3, Queen('white'))
        self.place_piece(7, 4, King('white'))
        for i in range(8):
            self.place_piece(1, i, Pawn('black'))
            self.place_piece(6, i, Pawn('white'))
        



