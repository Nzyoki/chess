import pygame
import os
from board import Board
from pieces import Pawn,Rook,Knight,Bishop,Queen,King


WIDTH, HEIGHT = 800, 800
ROWS,COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE,BLACK = (255, 255, 255), (0, 0, 0)
LIGHT_BROWN,DARK_BROWN = (153, 102, 51), (102, 51, 0)

class ChessGame:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess Game')
        self.board = Board()
        self.moves=[]
        self.selected_piece=None
        self.running=True
        self.piece_images=self.load_images()
        

        self.font=pygame.font.SysFont('Arial', 50)
        self.init_pieces()
    
    def load_images(self):
        pieces=['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors=['white', 'black']

        for piece in pieces:
            for color in colors:
                image_path=os.path.join('images', f'{color}_{piece}.png')

                try:
                    image=pygame.image.load(image_path)
                    image=pygame.transform.scale(image, (SQUARE_SIZE -10, SQUARE_SIZE -10))
                    self.piece_images[f'{color}_{piece}.png']=image
                except Exception as e:
                    print(f'cantload image: {image_path}')
                    print(f'Error:{e}')

                    placeholder=pygame.Surface((SQUARE_SIZE -10, SQUARE_SIZE -10))
                    placeholder.fill((255,0,0))
                    self.piece_images[f'{color}_{piece}.png']=placeholder
                
    
    def init_pieces(self):
        self.board.setup_pieces()
    
    def add_move(self,move):
        self.moves.append(move)

    def delete_move(self,index):
        if 0<=index < len(self.moves):
            del self.moves[index]

    def update_move(self,index,new_move):
        if 0<=index <len(self.moves):
            self.moves[index]=new_move

    def read_moves(self):
        return self.moves

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                color=LIGHT_BROWN if (row+col)%2==0 else DARK_BROWN
                pygame.draw.rect(self.screen, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece=self.board.board[row][col]
                if piece:
                    image=self.piece_images[piece.image_name]
                    if image:
                        x=col*SQUARE_SIZE + (SQUARE_SIZE -image.get_width())//2, 
                        y=row*SQUARE_SIZE + (SQUARE_SIZE - image.get_height())//2
                        self.screen.blit(image, (x, y))
                    # text=self.font.render(piece.symbol,True, BLACK if piece.color=='white' else WHITE)
                    # self.screen.blit(text,(col*SQUARE_SIZE+SQUARE_SIZE//3, row*SQUARE_SIZE+SQUARE_SIZE//4))
    
    def handle_click(self,x,y):
        row,col =y // SQUARE_SIZE, x // SQUARE_SIZE
        if self.selected_piece:
            start_x,start_y = self.selected_piece
            if self.board.move_piece(start_x, start_y, row, col):
                self.add_move((start_x, start_y, row, col))
                self.selected_piece=None
        else:
            if self.board.board[row][col]:
                self.selected_piece=(row, col)
    
    def run(self):
        clock=pygame.time.Clock()

        while self.running:
            clock.tick(60)
            self.screen.fill(WHITE)
            self.draw_board()
            self.draw_pieces()

            if self.selected_piece:
                row,col=self.selected_piece
                highlight_surface=pygame.Surface((SQUARE_SIZE, SQUARE_SIZE),pygame.SRCALPHA)
                highlight_surface.fill((255,0,0,100))
                self.screen.blit(highlight_surface, (col*SQUARE_SIZE, row*SQUARE_SIZE))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    self.handle_click(x,y)
        
        pygame.quit()

if __name__ == "__main__":
    game=ChessGame()
    game.run()



