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
        
        
        
    def draw_background(self, window):
        window.fill(WHITE)
        
        for row in range(ROWS):
            for col in range(row % 2, ROWS , 2): # Paint every other square
                pygame.draw.rect(window, BLACK, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) )

    def create_board(self): 
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                #print(row, col)
                if (col == 0 or col == COLS-1) and row!=0 and row != ROWS-1 :
                    self.board[row].append(Piece(row,col, BLUE))
                
                elif (row == 0 or row == ROWS-1) and col!=0 and col != COLS-1 :
                    self.board[row].append(Piece(row,col, RED))
                   
                else:
                    self.board[row].append(0) 
            
    def draw(self, window):
        self.draw_background(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if(piece!=0):
                    piece.draw(window)
                    
    def remove(self, piece):
        self.board[piece.row][piece.col] = 0
        
        if piece != 0:
            if piece.color == RED:
                self.red_left -=1
            else:
                self.blue_left -=1
                    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row,col)
        
    def get_piece(self, row, col):
        if( 0 <= col  < COLS and 0 <= row  < ROWS):
            return self.board[row][col]
        return 0
    
    def get_valid_moves(self, piece):
        moves = []
        
        hor_moves = 0
        ver_moves = 0
        for i in range (COLS):
            #horizontal
            if (self.board[piece.row][i] != 0):
                hor_moves+=1
            if (self.board[i][piece.col] != 0):
                ver_moves+=1
                
                
        #print("posso andar ", hor_moves ," casas na horizontal")
        #print("posso andar ", ver_moves ," casas na vertical")
        
        self.move_horizontal(piece,moves, hor_moves)
        self.move_vertical(piece,moves, ver_moves)
        
            
        
        return moves
    
    def move_horizontal(self, piece, moves, hor_moves):
        positiveValidMove = True
        negativeValidMove = True
        for i in range (1,hor_moves):
            temp1 = self.get_piece(piece.row,piece.col+i)
            temp2 = self.get_piece(piece.row,piece.col-i)
            
            # Other color piece blocking our play
            if(temp1 != 0  and piece.color != temp1.color):
                positiveValidMove = False
            
            if(temp2 != 0  and piece.color != temp2.color):
                negativeValidMove = False
        
        # Para impedir comer uma peça da propria cor na ultima posiçao
        # Caso contrario podemos "saltar" por cima delas por isso não há problema :) 
        temp1 = self.get_piece(piece.row,piece.col+hor_moves)        
        temp2 = self.get_piece(piece.row,piece.col-hor_moves)        
        if temp1 != 0 and temp1.color == piece.color:
            positiveValidMove = False
        if temp2 != 0 and temp2.color == piece.color:
            negativeValidMove = False

        if( positiveValidMove):
            moves.append( (piece.row, piece.col + hor_moves) )
            #print("ENTREI ", piece.row, piece.col + hor_moves)
        
        if( negativeValidMove ):
            moves.append( (piece.row, piece.col - hor_moves) )
            #print("ENTREI ", piece.row, piece.col - hor_moves)
            
    def move_vertical(self, piece, moves, ver_moves):
        positiveValidMove = True
        negativeValidMove = True
        
        for i in range (1, ver_moves):
            temp1 = self.get_piece(piece.row+i,piece.col)
            temp2 = self.get_piece(piece.row-i,piece.col)
            
            if temp1 != 0 and temp1.color != piece.color:
                positiveValidMove = False
            
            if temp2 != 0 and temp2.color != piece.color:
                negativeValidMove = False

        temp1 = self.get_piece(piece.row + ver_moves,piece.col)        
        temp2 = self.get_piece(piece.row - ver_moves,piece.col)
        
        if temp1 != 0 and temp1.color == piece.color:
            positiveValidMove = False
        
        if temp2 != 0 and temp2.color == piece.color:
            negativeValidMove = False

        if( positiveValidMove ):
            moves.append( (piece.row + ver_moves, piece.col) )
        
        if( negativeValidMove ):
            moves.append( (piece.row - ver_moves, piece.col) )