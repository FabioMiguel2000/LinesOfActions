from pickle import FALSE, TRUE
import pygame
import sys
from game.constants import *
from game.game import Game
from minimax.algorithm import minimax

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('Lines of Action')
icon = pygame.image.load('../img/logo.png')
pygame.display.set_icon(icon)

FPS = 60

BOT_WHITE = 0
BOT_BLACK = 0
NUMBER_OF_PLAYS = 1

# Receives the position clicked by mouse <pos>, finds out and returns
# the corresponding row and column clicked in the game board
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

# Receives the arguments passed from the command line and sets the game mode
def parse_args(args):
    global BOT_WHITE
    global BOT_BLACK
    global NUMBER_OF_PLAYS

    if len(args) != 4 and len(args) != 3:
        return False
    if args[1] == '-l1':
        BOT_WHITE = EASY_LEVEL
    elif args[1] == '-l2':
        BOT_WHITE = MEDIUM_LEVEL
    elif args[1] == '-l3':
        BOT_WHITE = HARD_LEVEL
    elif args[1] == '-h':
        BOT_WHITE = -1
    else:
        return False

    if args[2] == '-l1':
        BOT_BLACK = EASY_LEVEL
    elif args[2] == '-l2':
        BOT_BLACK = MEDIUM_LEVEL
    elif args[2] == '-l3':
        BOT_BLACK = HARD_LEVEL
    elif args[2] == '-h':
        BOT_BLACK = -1
    else:
        return False
    
    if len(args) == 4:
        if int(args[3]) > 0 and int(args[3]) < 1000:
            NUMBER_OF_PLAYS = int(args[3])
        else:
            return False

    return True
    


def main():
    if not(parse_args(sys.argv)):
        print("\nUsage: main.py <WhitePlayer> <BlackPlayer> [NGames]\n\n\n\t<WhitePlayer> and <BlackPlayer> options: \n\t\t-h : For Human Player \n\t\t-l1 : For Bot Player Easy Level, \n\t\t-l2 : For Bot Player Medium Level, \n\t\t-l3 : For Bot Player Hard Level\n\n\t[NGames] options: \n\t\t[1-1000] default=10 : Number of games to play, OPTIONAL\n\n\tex: main.py -l1 -h 30\n")
        return

    run = True                      # Game Loop Flag
    clock = pygame.time.Clock()     # Object to help track time
    game = Game(WINDOW)             # Pygame Window

    blackwins = 0
    whitewins= 0

    counter = 0
    # Event Loop
    while run and (counter < NUMBER_OF_PLAYS):
        clock.tick(FPS)             # Limits the game to run no more than <FPS> frames per second

        if game.turn == WHITE and BOT_WHITE != -1:
            # print("WHITE:", BOT_WHITE)
            value, new_board = minimax(game.get_board(), BOT_WHITE, True, game, WHITE, float('-inf'),  float('inf'))
            game.ai_move(new_board)
        elif game.turn == BLACK and BOT_BLACK != -1:
            # print("BLACK:", BOT_BLACK)
            value, new_board = minimax(game.get_board(), BOT_BLACK, True, game, BLACK, float('-inf'),  float('inf'))
            game.ai_move(new_board)

        gameStatus = game.check_gameover()

        if gameStatus != GAME_CONTINUE:
            if gameStatus == BLACK_WINS:
                print("BLACK WINS!")
                blackwins +=1
            else:
                print("WHITE WINS")
                whitewins +=1
            print(game.countMoves)
            game.update()
            # pygame.image.save(WINDOW, "endGame.png" )
            counter +=1
            game.reset()

        for event in pygame.event.get():                # Loop through game events
            if event.type == pygame.QUIT:               # EVENT - If window closed, then stop running
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:    # EVENT - Listener for mouse clicks
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)

                game.select(row, col)

        game.update()

    print("\nFINAL RESULT: ", whitewins, "-", blackwins, "(White-Black)\n")
    pygame.quit()


main()
