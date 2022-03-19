from re import S
import pygame
from game.constants import *
from game.piece import *


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None
        self.white_left = self.black_left = 12
        
        self.create_board()
        
        
        
    def draw_background(self, window):
        window.fill(WHITE)
        
        for row in range(ROWS):
            for col in range(row % 2, ROWS , 2): # Paint every other square
                pygame.draw.rect(window, BLACK, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE) )

    # Fiz um bocado à trolha, dá para melhorar isto
    # acho que basta 1 CICLO FOR pq queremos criar nas casas
    # AZUIS (0,1), (0,2)... 
    # VERMELHAS (1,0), (2,0)
    # E o contrario para o lado de baixo e direita  
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
                    
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row,col)
        
    def get_piece(self, row, col):
        return self.board[row][col]
    
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

        if( 0 <= piece.col + hor_moves <= COLS ):
            moves.append( (piece.row, piece.col + hor_moves) )
            #print("ENTREI ", piece.row, piece.col + hor_moves)
        
        if( 0 <= piece.col - hor_moves <= COLS ):
            moves.append( (piece.row, piece.col - hor_moves) )
            #print("ENTREI ", piece.row, piece.col - hor_moves)
            
    def move_vertical(self, piece, moves, ver_moves):

        if( 0 <= piece.row + ver_moves <= ROWS ):
            moves.append( (piece.row + ver_moves, piece.col) )
            print("ENTREI ", piece.row  + ver_moves, piece.col)
        
        if( 0 <= piece.row - ver_moves <= ROWS ):
            moves.append( (piece.row - ver_moves, piece.col) )
            print("ENTREI ", piece.row - ver_moves, piece.col)