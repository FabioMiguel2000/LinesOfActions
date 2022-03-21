from re import S
import pygame
from .constants import *
from .piece import *


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.blue_left = self.red_left = 12

        self.create_board()

    # Draws the game board, this includes the black and white squares
    def draw_background(self, window):
        window.fill(WHITE)

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):  # Paint every other square
                pygame.draw.rect(window, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Initializes the board, with the pieces on their initial position
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (col == 0 or col == COLS - 1) and row != 0 and row != ROWS - 1:
                    self.board[row].append(Piece(row, col, BLUE))

                elif (row == 0 or row == ROWS - 1) and col != 0 and col != COLS - 1:
                    self.board[row].append(Piece(row, col, RED))

                else:
                    self.board[row].append(0)

                    # Draws everything, board and pieces of the current game state

    def draw(self, window):
        self.draw_background(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)

    # Removes a piece from the board, mainly for captures
    def remove(self, piece):
        self.board[piece.row][piece.col] = 0

        if piece != 0:
            if piece.color == RED:
                self.red_left -= 1
            else:
                self.blue_left -= 1

    # Moves a piece to a new square
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    # Returns the piece on the given position, or 0 if it does not exist
    def get_piece(self, row, col):
        if 0 <= col < COLS and 0 <= row < ROWS:
            return self.board[row][col]
        return 0

    # Get all the valid moves of a given piece
    def get_valid_moves(self, piece):
        moves = []

        hor_moves = 0
        ver_moves = 0
        for i in range(COLS):
            if self.board[piece.row][i] != 0:
                hor_moves += 1          # Count pieces on the horizontal line
            if self.board[i][piece.col] != 0:
                ver_moves += 1          # Count pieces on the vertical column

        # print("posso andar ", hor_moves ," casas na horizontal")
        # print("posso andar ", ver_moves ," casas na vertical")

        self.move_horizontal(piece, moves, hor_moves)
        self.move_vertical(piece, moves, ver_moves)

        # Missing diagonal movement
        print(moves)
        return moves

    # Finds all horizontal valid moves of the piece
    def move_horizontal(self, piece, moves, hor_moves):
        positiveValidMove = True    # To the right
        negativeValidMove = True    # To the left
        for i in range(1, hor_moves + 1):
            temp1 = self.get_piece(piece.row, piece.col + i)
            temp2 = self.get_piece(piece.row, piece.col - i)

            # Other color piece blocking our play
            if i != hor_moves:
                if temp1 != 0 and piece.color != temp1.color:
                    positiveValidMove = False

                if (temp2 != 0 and piece.color != temp2.color):
                    negativeValidMove = False

            # Para impedir comer uma peça da propria cor na ultima posiçao
            # Caso contrario podemos "saltar" por cima delas por isso não há problema :)
            else:
                if temp1 != 0 and temp1.color == piece.color:
                    positiveValidMove = False

                if temp2 != 0 and temp2.color == piece.color:
                    negativeValidMove = False

        if (positiveValidMove):
            moves.append((piece.row, piece.col + hor_moves))
            # print("ENTREI ", piece.row, piece.col + hor_moves)

        if (negativeValidMove):
            moves.append((piece.row, piece.col - hor_moves))
            # print("ENTREI ", piece.row, piece.col - hor_moves)

    # Finds all vertical valid moves of the piece
    def move_vertical(self, piece, moves, ver_moves):
        positiveValidMove = True        # To the bottom
        negativeValidMove = True        # To the top

        for i in range(1, ver_moves + 1):
            temp1 = self.get_piece(piece.row + i, piece.col)
            temp2 = self.get_piece(piece.row - i, piece.col)

            if i != ver_moves:
                if temp1 != 0 and temp1.color != piece.color:
                    positiveValidMove = False

                if temp2 != 0 and temp2.color != piece.color:
                    negativeValidMove = False
            else:
                if temp1 != 0 and temp1.color == piece.color:
                    positiveValidMove = False

                if temp2 != 0 and temp2.color == piece.color:
                    negativeValidMove = False

        if (positiveValidMove):
            moves.append((piece.row + ver_moves, piece.col))

        if (negativeValidMove):
            moves.append((piece.row - ver_moves, piece.col))
