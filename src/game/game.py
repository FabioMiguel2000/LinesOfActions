import pygame
from .board import Board
from .constants import *


class Game:
    def __init__(self, window):
        self.window = window
        self.reset()

    # Function to update the game view
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    # Resets/initializes the game states
    def reset(self):
        self.selected = None       # The current selected piece
        self.board = Board()       # Game board object
        self.turn = BLACK           # The current player turn
        self.valid_moves = {}      # List of all valid moves

    # Given the row and column clicked by the mouse, depending on the current condition
    # it can either move a piece on the board or select a piece
    def select(self, row, col):
        if self.selected:                   # piece is already selected
            result = self.move(row, col)    # move piece if it is a valid move

            if not result:                  # if not valid move
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:     # If valid move and player's turn
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
                
            return True
        
        return False

    # Moves the selected piece if it is a valid move
    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        
        if self.selected and (row, col) in self.valid_moves:   # If it is a valid move
            if piece != 0:              # If it is a capture move
                self.board.remove(piece)

            self.board.move(self.selected, row, col)    # Moves the piece
            self.change_turn()

        else:
            return False

        return True

    # Marks on the board the valid moves by the piece (Green Dot)
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 ), 15 )

    # Changes the player turn
    def change_turn(self):
        self.refresh_state()
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
            
    # Refreshes the state
    def refresh_state(self):
        self.selected = None;
        self.valid_moves = [];

        