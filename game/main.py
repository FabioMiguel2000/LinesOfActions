import pygame
from game.constants import *
from game.board import Board

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Lines of Action')

FPS = 60

def get_row_col_from_mouse(pos):
    x, y = pos
    row =  y // SQUARE_SIZE
    col =  x // SQUARE_SIZE
    return row,col
    

def main():
    run = True
    clock = pygame.time.Clock()
    board = Board()
    
    # piece = board.get_piece(0,1)
    # 
    
    # Event Loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                piece = board.get_piece(row,col)
                
                board.move(piece, 4,4)
            
        board.draw(WINDOW)
        pygame.display.update()
                
    pygame.quit()
    
main()