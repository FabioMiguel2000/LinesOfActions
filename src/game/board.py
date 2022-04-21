import pygame
import random

from .constants import *
from .piece import *

incX = [-1,+1, 0, 0,-1,-1,+1,+1]
incY = [ 0, 0,-1,+1,-1,+1,-1,+1]  


class Board:
        
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.black_left = self.white_left = 12
        
        self.counter = 0
        self.maxSoFar = 0
        self.visited = []

        self.create_board()

    # Draws the game board, this includes the black and white squares
    def draw_background(self, window):
        window.fill(BOARD_COLOR_1)

        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):  # Paint every other square
                pygame.draw.rect(window, BOARD_COLOR_2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Initializes the board, with the pieces on their initial position
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if (col == 0 or col == COLS - 1) and row != 0 and row != ROWS - 1:
                    self.board[row].append(Piece(row, col, WHITE))

                elif (row == 0 or row == ROWS - 1) and col != 0 and col != COLS - 1:
                    self.board[row].append(Piece(row, col, BLACK))

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
            if piece.color == BLACK:
                self.black_left -= 1
            else:
                self.white_left -= 1

    # def winner(self):
    #     # TODO
    #     return None

    # Moves a piece to a new square and checks if a player or the other has won
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    # Returns the piece on the given position, or 0 if it does not exist
    def get_piece(self, row, col):
        if 0 <= col < COLS and 0 <= row < ROWS:
            return self.board[row][col]
        return 0

    #       ------------ Heuristic Evaluation Methods ---------------
    def evaluate(self, turn):
        
        pieces = self.get_all_pieces(turn)
        value = self.centralisation(pieces)
        # print("Centralization value: ", value)
        value += self.maxGroupSize(turn) * 1000
        concentrationVal = self.concentration(pieces)
        randomVal = random.randint(0,5)
        value += concentrationVal + randomVal
        # print("concentration value: ", concentrationVal)

        return value

    def centralisation(self, pieces):
        pieceSquareTable = [[-80, -25, -20, -20, -20, -20, -25, -80],
            [-25,  10,  10,  10,  10,  10,  10, -25],
                [-20,  10,  25,  25,  25,  25,  10, -20],
                [-20,  10,  25,  50,  50,  25,  10, -20],
                [-20,  10,  25,  50,  50,  25,  10, -20],
                [-20,  10,  25,  25,  25,  25,  10, -20],
                [-25,  10,  10,  10,  10,  10,  10, -25],
                [-80, -25, -20, -20, -20, -20, -25, -80]]

        sum = 0

        for piece in pieces:
            sum += pieceSquareTable[piece.row][piece.col]

        return sum

    def concentration(self, pieces):
        centerRow = 0
        centerCol = 0

        for piece in pieces:
            centerRow += piece.row
            centerCol += piece.col
        
        centerRow /= len(pieces)
        centerCol /= len(pieces)
        totalDistance = 0
        for piece in pieces:
            totalDistance += max(abs(centerRow-piece.row), abs(centerCol-piece.col))

        averageDistance = totalDistance/len(pieces)

        return -100*averageDistance

    def maxGroupSize(self, turn):
        self.counter = 0
        self.maxSoFar = 0
        self.visited = []
        
        for row in range(ROWS):
            self.visited.append([])
            for col in range(COLS):
                self.visited[row].append(False)
                
        for row in range(ROWS):
            for col in range(COLS):
                tempiece = self.get_piece(row,col) 
                if tempiece != 0 and tempiece.color == turn and not self.visited[row][col]:
                   self.counter = 0
                   #print(row, col)
                   self.dfs(row,col, turn)

                # MELHORAR ISTO
                #nao quero saber a maior, mas sim se apenas existe uma
                # if self.counter > self.maxSoFar:
                #     self.maxSoFar = self.counter
                self.maxSoFar = max(self.counter, self.maxSoFar)
        # print("HEY I FOUND " , self.maxSoFar, " for ","black" if colorPlayed==(0,0,0) else "white")
        return self.maxSoFar

    def dfs(self, row, col, colorPiece):
        if not (0 <= col < COLS and 0 <= row < ROWS) or self.visited[row][col]: return

        tempiece = self.get_piece(row, col)
        if tempiece == 0 or tempiece.color != colorPiece: return

        self.visited[row][col] = True
        self.counter += 1
        for i in range(8):
            self.dfs(row + incX[i], col + incY[i], colorPiece)

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

        diag_botright_moves = 1
        diag_botleft_moves = 1
        # top-left
        for i in range(1, min(piece.col, piece.row)+1):
            if self.get_piece(piece.row-i, piece.col-i) != 0:
                diag_botright_moves += 1
        # bot-right
        for i in range(1, min(COLS - piece.col, ROWS - piece.row)):
            if self.get_piece(piece.row+i, piece.col+i) != 0:
                diag_botright_moves += 1
        # top-right
        for i in range(1, min(COLS - piece.col, piece.row) + 1):
            if self.get_piece(piece.row-i, piece.col+i) != 0:
                diag_botleft_moves += 1
        # bot-left
        for i in range(1, min(piece.col, ROWS - piece.row) + 1):
            if self.get_piece(piece.row+i, piece.col-i) != 0:
                diag_botleft_moves += 1

        self.move_horizontal(piece, moves, hor_moves)
        self.move_vertical(piece, moves, ver_moves)

        self.move_bot_right(piece, moves, diag_botright_moves)
        self.move_bot_left(piece, moves, diag_botleft_moves)

        # print(moves)

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

        if positiveValidMove and (piece.col + hor_moves < COLS):
            moves.append((piece.row, piece.col + hor_moves))
            # print("ENTREI ", piece.row, piece.col + hor_moves)

        if negativeValidMove and (piece.col - hor_moves) >= 0:
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

        if positiveValidMove and (piece.row + ver_moves < ROWS):
            moves.append((piece.row + ver_moves, piece.col))

        if negativeValidMove and (piece.row - ver_moves >= 0):
            moves.append((piece.row - ver_moves, piece.col))

    def move_bot_right(self, piece, moves, diag_botright_moves):
        positiveValidMove = True  # To the bottom right
        negativeValidMove = True  # To the top left
        for i in range(1, diag_botright_moves+1):
            cell_element1 = self.get_piece(piece.row + i, piece.col + i)
            cell_element2 = self.get_piece(piece.row - i, piece.col - i)
            if i < diag_botright_moves:
                if cell_element1 != 0 and piece.color != cell_element1.color:
                   positiveValidMove = False

                if cell_element2 != 0 and piece.color != cell_element2.color:
                    negativeValidMove = False

            else:
                if cell_element1 != 0 and cell_element1.color == piece.color:
                    positiveValidMove = False

                if cell_element2 != 0 and cell_element2.color == piece.color:
                    negativeValidMove = False

        if positiveValidMove and (piece.col + diag_botright_moves < COLS) and (piece.row + diag_botright_moves < ROWS):
            moves.append((piece.row+ diag_botright_moves, piece.col + diag_botright_moves))

        if negativeValidMove and (piece.col - diag_botright_moves >= 0) and (piece.row - diag_botright_moves >= 0):
            moves.append((piece.row- diag_botright_moves, piece.col - diag_botright_moves))


    def move_bot_left(self, piece, moves, diag_botleft_moves):
        positiveValidMove = True  # To the bottom left
        negativeValidMove = True  # To the top right
        for i in range(1, diag_botleft_moves+1):
            cell_element1 = self.get_piece(piece.row + i, piece.col - i)
            cell_element2 = self.get_piece(piece.row - i, piece.col + i)
            if i < diag_botleft_moves: # not final position
                if cell_element1 != 0 and piece.color != cell_element1.color: # enemy piece
                   positiveValidMove = False

                if cell_element2 != 0 and piece.color != cell_element2.color: # enemy piece
                    negativeValidMove = False

            else:
                if cell_element1 != 0 and cell_element1.color == piece.color:
                    positiveValidMove = False

                if cell_element2 != 0 and cell_element2.color == piece.color:
                    negativeValidMove = False

        if positiveValidMove and (piece.col - diag_botleft_moves >= 0) and (piece.row + diag_botleft_moves < ROWS):
            moves.append((piece.row + diag_botleft_moves, piece.col - diag_botleft_moves))

        if negativeValidMove and (piece.col + diag_botleft_moves < COLS) and (piece.row - diag_botleft_moves >= 0):
            moves.append((piece.row - diag_botleft_moves, piece.col + diag_botleft_moves))



