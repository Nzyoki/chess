import pygame
import sys
from board import Board
import random
import json
import os
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 800
SQUARE_SIZE = WINDOW_SIZE // 8

# Enhanced Color Scheme for the chess board
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_WOOD = (120, 81, 45)    
LIGHT_WOOD = (205, 170, 125) 
GOLD = (255, 215, 0)
HIGHLIGHT = (255, 255, 0, 128)
SCOREBOARD_BG = (245, 245, 245)  
DARK_BLUE = (25, 25, 112)    
FOREST_GREEN = (34, 139, 34)
CRIMSON = (220, 20, 60)      
MOVE_HIGHLIGHT = (124, 252, 0, 128)  

# Set up the display
screen = pygame.display.set_mode((WINDOW_SIZE + 250, WINDOW_SIZE))
pygame.display.set_caption('Chess Game')

def create_gradient_surface(width, height, start_color, end_color):
   
    surface = pygame.Surface((width, height))
    for y in range(height):
        ratio = y / height
        color = [start + (end - start) * ratio for start, end in zip(start_color, end_color)]
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.board.setup_pieces()
        self.selected_piece = None
        self.selected_pos = None
        self.game_id = self.get_next_game_id()
        self.piece_images = {}
        self.scores = self.load_scores()
        self.current_score = {'white': 0, 'black': 0}
        self.game_history = []
        self.show_scoreboard = False
        self.load_pieces()
        self.load_game_state()
        self.board_border = 10  # Border width for the chess board
        self.gradient_bg = create_gradient_surface(250, WINDOW_SIZE, 
                                                 (245, 245, 245), (220, 220, 220))
#method to get the next game id
    def get_next_game_id(self):
       
        try:
            with open('scores.json', 'r') as f:
                scores = json.load(f)
                return max([score['game_id'] for score in scores], default=-1) + 1
        except FileNotFoundError:
            return 0
# method to load the pieces from the assets folder
    def load_pieces(self):
        piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        for piece in piece_types:
            for color in colors:
                try:
                    img_path = os.path.join('assets', f'{color}-{piece}.png')
                    img = pygame.image.load(img_path)
                    
                    self.piece_images[f'{color}_{piece}'] = pygame.transform.scale(
                        img, (SQUARE_SIZE, SQUARE_SIZE))
                except Exception as e:
                    print(f"Error loading {color}-{piece}.png: {e}")
                    
                    surf = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    pygame.draw.circle(surf, (*((255, 255, 255) if color == 'white' else (0, 0, 0)), 128),
                                    (SQUARE_SIZE//2, SQUARE_SIZE//2), SQUARE_SIZE//3)
                    self.piece_images[f'{color}_{piece}'] = surf

#method to load the scores from the scores.json file
    def load_scores(self):
       
        try:
            with open('scores.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
#method to save the scores to the scores.json file
    def save_scores(self):
        
        with open('scores.json', 'w') as f:
            json.dump(self.scores, f, indent=4)
#method to add a new game result to the scores.json file
    def add_game_result(self, winner, moves):
       
        game_record = {
            'game_id': self.game_id,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'winner': winner,
            'white_score': self.current_score['white'],
            'black_score': self.current_score['black'],
            'moves': moves,
            'total_moves': len(moves)
        }
        self.scores.append(game_record)
        self.save_scores()
        print(f"Game {self.game_id} saved!")
#method to delete a specific game record from the scores.json file
    def delete_game_record(self, game_id):
        initial_length = len(self.scores)
        self.scores = [score for score in self.scores if score['game_id'] != game_id]
        if len(self.scores) < initial_length:
            self.save_scores()
            print(f"Game {game_id} deleted!")
        else:
            print(f"Game {game_id} not found!")
#method to update a specific game record in the scores.json file
    def update_game_record(self, game_id, winner=None):
      
        for score in self.scores:
            if score['game_id'] == game_id:
                if winner:
                    score['winner'] = winner
                score['white_score'] = self.current_score['white']
                score['black_score'] = self.current_score['black']
                score['moves'] = self.game_history
                score['total_moves'] = len(self.game_history)
                self.save_scores()
                print(f"Game {game_id} updated!")
                return True
        print(f"Game {game_id} not found!")
        return False
#method to calculate the piece value for scoring
    def calculate_piece_value(self, piece):
       
        values = {
            'Pawn': 1,
            'Knight': 3,
            'Bishop': 3,
            'Rook': 5,
            'Queen': 9,
            'King': 0  # King's capture ends the game
        }
        return values.get(piece.__class__.__name__, 0)
#method to move the piece on the board
    def move_piece(self, start_x, start_y, end_x, end_y):
       
        target_piece = self.board.get_piece(end_x, end_y)
        if target_piece:  # If capturing a piece
            self.current_score[self.board.current_turn] += self.calculate_piece_value(target_piece)
            # Record the move in game history
            self.game_history.append({
                'move': (start_x, start_y, end_x, end_y),
                'piece_captured': str(target_piece.__class__.__name__),
                'turn': self.board.current_turn
            })
        
        # Perform the actual move
        return self.board.move_piece(start_x, start_y, end_x, end_y)
#method to save the game state to the game_state.json file
    def save_game_state(self):
        game_state = {
            'board': [[str(piece.__class__.__name__) + "_" + piece.color if piece else None 
                      for piece in row] for row in self.board.board],
            'current_turn': self.board.current_turn,
            'game_id': self.game_id,
            'current_score': self.current_score,
            'game_history': self.game_history
        }
        with open('game_state.json', 'w') as f:
            json.dump(game_state, f)

    def load_game_state(self):
    
        try:
            with open('game_state.json', 'r') as f:
                game_state = json.load(f)
                self.game_id = game_state['game_id']
                self.board.current_turn = game_state['current_turn']
                self.current_score = game_state.get('current_score', {'white': 0, 'black': 0})
                self.game_history = game_state.get('game_history', [])
                # Reconstruct board from saved state
                for i, row in enumerate(game_state['board']):
                    for j, piece_str in enumerate(row):
                        if piece_str:
                            piece_name, color = piece_str.split('_')
                            piece_class = getattr(__import__('pieces'), piece_name)
                            self.board.board[i][j] = piece_class(color)
        except FileNotFoundError:
            self.board.setup_pieces()

    def delete_game_state(self):
       
        if os.path.exists('game_state.json'):
            os.remove('game_state.json')
        self.game_id += 1
        self.board = Board()
        self.board.setup_pieces()
        self.selected_piece = None
        self.selected_pos = None
        self.current_score = {'white': 0, 'black': 0}
        self.game_history = []

    def draw_fancy_rect(self, surface, color, rect, border_radius=15):
        
        pygame.draw.rect(surface, color, rect, border_radius=border_radius)

    def draw_scoreboard(self):
     
        screen.blit(self.gradient_bg, (WINDOW_SIZE, 0))
        
        
        pygame.draw.rect(screen, DARK_BLUE, (WINDOW_SIZE-2, 0, 4, WINDOW_SIZE))
        
        # Title section with fancy background
        title_rect = pygame.Rect(WINDOW_SIZE + 10, 5, 230, 40)
        self.draw_fancy_rect(screen, DARK_BLUE, title_rect)
        
        font_title = pygame.font.SysFont('Arial', 24, bold=True)
        font_regular = pygame.font.SysFont('Arial', 20)
        font_small = pygame.font.SysFont('Arial', 18)
        
        # Main title
        title = font_title.render('CHESS SCOREBOARD', True, GOLD)
        screen.blit(title, (WINDOW_SIZE + 25, 12))
        
        # Current game section
        current_section = pygame.Rect(WINDOW_SIZE + 10, 55, 230, 100)
        self.draw_fancy_rect(screen, (240, 240, 240), current_section)
        
        current_title = font_regular.render('Current Game', True, DARK_BLUE)
        screen.blit(current_title, (WINDOW_SIZE + 25, 65))
        
        # Current scores with enhanced styling
        score_bg = pygame.Rect(WINDOW_SIZE + 20, 95, 210, 50)
        self.draw_fancy_rect(screen, WHITE, score_bg)
        
        white_score = font_regular.render(f'White: {self.current_score["white"]}', True, BLACK)
        black_score = font_regular.render(f'Black: {self.current_score["black"]}', True, BLACK)
        screen.blit(white_score, (WINDOW_SIZE + 30, 100))
        screen.blit(black_score, (WINDOW_SIZE + 30, 120))
        
        # Recent games section
        recent_title = font_regular.render('Recent Games', True, DARK_BLUE)
        screen.blit(recent_title, (WINDOW_SIZE + 25, 170))
        
        y_pos = 200
        for score in sorted(self.scores[-5:], key=lambda x: x['game_id'], reverse=True):
            # Game record background
            record_bg = pygame.Rect(WINDOW_SIZE + 10, y_pos, 230, 80)
            self.draw_fancy_rect(screen, WHITE, record_bg)
            
            game_text = font_small.render(f'Game {score["game_id"]}', True, DARK_BLUE)
            winner_color = FOREST_GREEN if score["winner"] == "white" else CRIMSON
            winner_text = font_small.render(f'Winner: {score["winner"]}', True, winner_color)
            score_text = font_small.render(f'W:{score["white_score"]} B:{score["black_score"]}', True, BLACK)
            moves_text = font_small.render(f'Moves: {score.get("total_moves", 0)}', True, DARK_BLUE)
            
            screen.blit(game_text, (WINDOW_SIZE + 20, y_pos + 5))
            screen.blit(winner_text, (WINDOW_SIZE + 20, y_pos + 25))
            screen.blit(score_text, (WINDOW_SIZE + 20, y_pos + 45))
            screen.blit(moves_text, (WINDOW_SIZE + 20, y_pos + 65))
            
            y_pos += 90

    def draw_board(self):
        # Draw board border
        pygame.draw.rect(screen, DARK_BLUE, 
                        (0, 0, WINDOW_SIZE, WINDOW_SIZE))
        
        # Draw squares with wood-like colors
        for row in range(8):
            for col in range(8):
                color = LIGHT_WOOD if (row + col) % 2 == 0 else DARK_WOOD
                pygame.draw.rect(screen, color,
                               (col * SQUARE_SIZE + 2, row * SQUARE_SIZE + 2,
                                SQUARE_SIZE - 4, SQUARE_SIZE - 4))
                
                piece = self.board.get_piece(row, col)
                if piece:
                    piece_type = piece.__class__.__name__.lower()
                    image = self.piece_images[f'{piece.color}_{piece_type}']
                    screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

        # Draw coordinates
        font = pygame.font.SysFont('Arial', 12)
        for i in range(8):
            # Draw rank numbers (1-8)
            rank = font.render(str(8-i), True, GOLD)
            screen.blit(rank, (5, i * SQUARE_SIZE + SQUARE_SIZE//2 - 6))
            
            # Draw file letters (a-h)
            file = font.render(chr(97 + i), True, GOLD)
            screen.blit(file, (i * SQUARE_SIZE + SQUARE_SIZE//2 - 4, WINDOW_SIZE - 15))

        # Highlight selected piece
        if self.selected_pos:
            row, col = self.selected_pos
            highlight = pygame.Surface((SQUARE_SIZE-4, SQUARE_SIZE-4), pygame.SRCALPHA)
            pygame.draw.rect(highlight, HIGHLIGHT, highlight.get_rect())
            screen.blit(highlight, (col * SQUARE_SIZE+2, row * SQUARE_SIZE+2))

    def cpu_move(self):
     
# First priority: Try to capture a piece
        for start_x in range(8):
            for start_y in range(8):
                piece = self.board.get_piece(start_x, start_y)
                if piece and piece.color == 'black':
                    # Look for possible captures
                    for end_x in range(8):
                        for end_y in range(8):
                            target = self.board.get_piece(end_x, end_y)
                            if target and target.color == 'white':
                                if piece.is_valid_move(self.board, start_x, start_y, end_x, end_y):
                                    # Make the capture move
                                    self.move_piece(start_x, start_y, end_x, end_y)
                                    return

# Second priority: Make any valid move
        valid_moves = []
        for start_x in range(8):
            for start_y in range(8):
                piece = self.board.get_piece(start_x, start_y)
                if piece and piece.color == 'black':
                    for end_x in range(8):
                        for end_y in range(8):
                            if piece.is_valid_move(self.board, start_x, start_y, end_x, end_y):
                                valid_moves.append((start_x, start_y, end_x, end_y))
        
# Make a random move if any valid moves exist
        if valid_moves:
            start_x, start_y, end_x, end_y = random.choice(valid_moves)
            self.move_piece(start_x, start_y, end_x, end_y)

    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_game_state()
                    if self.current_score['white'] != 0 or self.current_score['black'] != 0:
                        winner = 'white' if self.current_score['white'] > self.current_score['black'] else 'black'
                        self.add_game_result(winner, self.game_history)
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:  # New game
                        if self.current_score['white'] != 0 or self.current_score['black'] != 0:
                            winner = 'white' if self.current_score['white'] > self.current_score['black'] else 'black'
                            self.add_game_result(winner, self.game_history)
                        self.delete_game_state()
                    elif event.key == pygame.K_s:  # Save game
                        self.save_game_state()
                        self.update_game_record(self.game_id)
                    elif event.key == pygame.K_l:  # Load game
                        self.load_game_state()
                    elif event.key == pygame.K_d:  # Delete current game
                        self.delete_game_record(self.game_id)
                        self.delete_game_state()
                    elif event.key == pygame.K_h:  # Toggle scoreboard
                        self.show_scoreboard = not self.show_scoreboard
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.board.current_turn == 'white':
                    x, y = pygame.mouse.get_pos()
                    if x < WINDOW_SIZE:  # Only process clicks on the chess board
                        col = x // SQUARE_SIZE
                        row = y // SQUARE_SIZE
                        
                        clicked_piece = self.board.get_piece(row, col)
                        
                        if self.selected_piece:
                            if self.move_piece(self.selected_pos[0], self.selected_pos[1], row, col):
                                self.selected_piece = None
                                self.selected_pos = None
                                self.cpu_move()
                            else:
                                if clicked_piece and clicked_piece.color == 'white':
                                    self.selected_piece = clicked_piece
                                    self.selected_pos = (row, col)
                                else:
                                    self.selected_piece = None
                                    self.selected_pos = None
                        else:
                            if clicked_piece and clicked_piece.color == 'white':
                                self.selected_piece = clicked_piece
                                self.selected_pos = (row, col)

            screen.fill(DARK_BLUE) 
            self.draw_board()
            self.draw_scoreboard()
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    game = ChessGame()
    game.run() 