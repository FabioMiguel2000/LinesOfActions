import pygame
from game.constants import *
from game.game import Game
from minimax.algorithm import minimax

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Lines of Action')

FPS = 60


# Receives the position clicked by mouse <pos>, finds out and returns
# the corresponding row and column clicked in the game board
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True                      # Game Loop Flag
    clock = pygame.time.Clock()     # Object to help track time
    game = Game(WINDOW)             # Pygame Window

    # piece = board.get_piece(0,1)
    # 

    # Event Loop
    while run:
        clock.tick(FPS)             # Limits the game to run no more than <FPS> frames per second
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 2, WHITE, game)
            game.ai_move(new_board)
        
        # TODO ## aqui é que fica a logica do endgame
        # if game.winner() != None:
        #     print(game.winner())
        #     run = False) != None:
        #     print(game.winner())
        #     run = False
        
        for event in pygame.event.get():                # Loop through game events
            if event.type == pygame.QUIT:               # EVENT - If window closed, then stop running
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:    # EVENT - Listener for mouse clicks
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

                game.select(row, col)

        game.update()

    pygame.quit()


main()
