import pygame
from game.board import Board
from game.constants import BLUE, RED


class Game:
    def __init__(self, window):
        self.window = window
        self.reset()
        
    def update(self):
        self.board.draw(self.window)
        pygame.display.update()
        
    def reset(self):
        self.selected = None
        self.board = Board()
        self.turn = BLUE
        self.valid_moves = {}
        
    def select(self, row, col):
        print(row, col)
        if self.selected: 
            result = self.move(row,col)
            
            if not result:
                self.selected = None
                self.select(row,col)
        
        # precisa de else??        
        piece = self.board.get_piece(row,col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            
            return True
        
        return False
                
        
    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        
        if self.selected and (row,col) in self.valid_moves:
            print("MOVE")
            self.board.move(self.selected, row, col)
            self.change_turn()
        else:
            return False
        
        return True
    
    def change_turn(self):
        if self.turn == BLUE:
            self.turn = RED
        else:
            self.turn = BLUE
            
        
        

        