import pygame
from .board import Board
from .constants import RED, BLUE, GREEN, SQUARE_SIZE


class Game:
    def __init__(self, window):
        self.window = window
        self.reset()
        
    def update(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    def reset(self):
        self.selected = None
        self.board = Board()
        self.turn = BLUE
        self.valid_moves = {}
        
    def select(self, row, col):
        #print("SELECT ", row, col)
        if self.selected: 
            result = self.move(row,col)
            
            if not result:
                self.selected = None
                self.select(row,col)
        
        piece = self.board.get_piece(row,col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
                
            return True
        
        return False
                
        
    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        
        if self.selected and (row,col) in self.valid_moves:
            if(piece != 0):
                self.board.remove(piece)
            
            #print("MOVE")
            self.board.move(self.selected, row, col)
            self.change_turn()

        else:
            return False

        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2 ), 15 )
    
    def change_turn(self):
        self.refresh_state()
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE
            
        
    def refresh_state(self):
        self.selected = None;
        self.valid_moves = [];

        