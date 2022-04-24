import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

# RGB Values
BOARD_COLOR_1 = (221, 153, 68)
BOARD_COLOR_2 = (230, 185, 130)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

# Flag to decide if alpha-beta pruning should be used in minimax algorithm
ALPHA_BETA = True


# BOT LEVELS, the number represents the minimax algorithm DEPTH
EASY_LEVEL = 2
MEDIUM_LEVEL = 3
HARD_LEVEL = 4

# GAMESTATES
GAME_CONTINUE = -1
BLACK_WINS = 1
WHITE_WINS = 2


