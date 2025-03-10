class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_turn = 'white'  # Track whose turn it is
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        
    def get_piece(self, row, col):
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None

    def is_valid_position(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def place_piece(self, row, col, piece):
        if self.is_valid_position(row, col):
            self.board[row][col] = piece
            # Track king positions
            if piece.__class__.__name__ == 'King':
                if piece.color == 'white':
                    self.white_king_pos = (row, col)
                else:
                    self.black_king_pos = (row, col)
            return True
        return False

    def is_in_check(self, color):
        king_pos = self.white_king_pos if color == 'white' else self.black_king_pos
        
        # Check if any opponent piece can capture the king
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color != color:
                    if piece.is_valid_move(self, row, col, king_pos[0], king_pos[1]):
                        return True
        return False

    def would_be_in_check(self, start_x, start_y, end_x, end_y):
        # Temporarily make move and check if it results in check
        piece = self.board[start_x][start_y]
        temp_piece = self.board[end_x][end_y]
        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = None
        
        # Update king position if moving king
        original_king_pos = None
        if piece.__class__.__name__ == 'King':
            if piece.color == 'white':
                original_king_pos = self.white_king_pos
                self.white_king_pos = (end_x, end_y)
            else:
                original_king_pos = self.black_king_pos
                self.black_king_pos = (end_x, end_y)
        
        in_check = self.is_in_check(piece.color)
        
        # Restore board state
        self.board[start_x][start_y] = piece
        self.board[end_x][end_y] = temp_piece
        
        # Restore king position if it was moved
        if original_king_pos:
            if piece.color == 'white':
                self.white_king_pos = original_king_pos
            else:
                self.black_king_pos = original_king_pos
        
        return in_check

    def move_piece(self, start_x, start_y, end_x, end_y):
        if not (self.is_valid_position(start_x, start_y) and self.is_valid_position(end_x, end_y)):
            return False
            
        piece = self.board[start_x][start_y]
        if not piece or piece.color != self.current_turn:
            return False
            
        # Check if move is valid according to piece rules
        if not piece.is_valid_move(self, start_x, start_y, end_x, end_y):
            return False
            
        # Check if move would result in check
        if self.would_be_in_check(start_x, start_y, end_x, end_y):
            return False
            
        # Make the move
        self.board[end_x][end_y] = piece
        self.board[start_x][start_y] = None
        piece.has_moved = True
        
        # Update king position if moving king
        if piece.__class__.__name__ == 'King':
            if piece.color == 'white':
                self.white_king_pos = (end_x, end_y)
            else:
                self.black_king_pos = (end_x, end_y)
        
        # Handle pawn promotion
        if piece.__class__.__name__ == 'Pawn':
            if (piece.color == 'white' and end_x == 0) or (piece.color == 'black' and end_x == 7):
                from pieces import Queen
                self.board[end_x][end_y] = Queen(piece.color)
        
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'
        return True
    
    def setup_pieces(self):
        from pieces import Pawn, Rook, Knight, Bishop, Queen, King
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
