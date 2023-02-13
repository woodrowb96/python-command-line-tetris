"""
this file contains the class used to describe the screen that the tetris game is played on
"""

from Screen_objects import Block,Box,Block_heap,Block_box,Multi_line_text,Game_board,Background
from Shape import Shape,J,L,T,Line,Square,S,Z
from Settings import Dim,Symbols,Text,Movement

import os
import time
import random
import copy



CORNER = [0,0] #the screens corner 

#locatio nof the game board
BOARD_LOCATION = [1,1]  

#constants for the next block box
NEXT_BLOCK_LOCATION = [13,13]
BOX_W = 6   #box is 6 spaces wide and high
BOX_H = 6

LEVEL_LOCATION = [13,9]

SCORE_LOCATION = [13,5]

def random_shape():
    """this class returns a random shape"""
    return random.choice([J(),Square(),L(),T(),Line(),S(),Z()]) 

class Screen():
    """
    The screen class describes the screen on which a game of tetris is played 
    
    The screen is made up of the following objects from the screen_object file
        game_board:the game board where tetris is actually played. This is where the falling block
            controlled by the player is, and the block heap the block falls into 
        next_block: a box showing the next block the player controls after the current falling falls into place
        level:text displaying the current level
        score:text displaying the current score
        background:background that spans the entier screen

    """
   
    def __init__(self,level = 0,score = 0):
        self.game_board = Game_board(random_shape(),Dim.BOARD_H,Dim.BOARD_W,BOARD_LOCATION,Symbols.BOARDER)
        self.next_block = Block_box(random_shape(),BOX_H,BOX_W,Text.NEXT_BLOCK,NEXT_BLOCK_LOCATION,Symbols.BOX)
        self._level = Multi_line_text(LEVEL_LOCATION,[Text.LEVEL,str(level)])
        self._score = Multi_line_text(SCORE_LOCATION,[Text.SCORE,str(score)])
        self.background = Background(Dim.SCREEN_H + 1,Dim.SCREEN_W + 1,CORNER,Symbols.BLANK)

        #all objects on screen are collected in this list 
        self.objects = [self.game_board,self.next_block,self._level,self._score,self.background]
 
    def __getitem__(self,coord):
        """if there is an object on screen at coord return its symbol, else return None"""
        for obj in self.objects:
            symbol = obj[coord]
            if symbol:
                return symbol
    @property
    def level(self):
        return int(self._level)

    @level.setter   
    def level(self,level):
        """can set level by assigning it an int,then converting to string"""
        self._level[1] = str(level)
 
    @property
    def score(self):
        return int(self._score)

    @score.setter
    def score(self,score):
        """can set level by assigning it an int,then converting"""
        self._score[1] = str(score)
 
    def move_block(self,direction): 
        """
            this function tries to move the falling block, 
            it also handles the invalidmove and addtoheap exceptions
            this function returns true if move was succesfull, and false if not
        """  
        #try and move block to new location, check if that cause any exceptions
        #to be throw, then fix those exceptions
        try:
            self.game_board.move_block(direction)
            return True
        except Game_board.AddToHeap:    #if block should be added to heap
            self.game_board.un_move_block(direction)    #undo the last move
            self.switch_blocks()    #add block to heap,and get next falling block
            return False
        except Game_board.InvalidMove:  #if move was invalid
            self.game_board.un_move_block(direction)    #undo the last move
            return False

    def switch_blocks(self):
        """
            this function add the current falling block to the block heap
            turns the next_block into the next falling block
            and randomly generates a new next_block
        """  
        self.game_board.add_block_to_heap()
        self.game_board.block = self.next_block.block
        self.next_block.block = random_shape()

    def rotate_block(self):
        try:
            self.game_board.rotate_block()
        except Game_board.InvalidMove:
            self.game_board.un_rotate_block()
   
    def drop_block(self):
        #move block down until there has been an invalid move
        while self.move_block(Movement.DOWN): pass
                          
    def get_full_rows(self):
        """returns a list of full rows in the block heap"""
        return self.game_board.block_heap.get_full_rows()
   
    def set_full_rows(self,rows):
        """sets the full rows in block heap to there full symbol"""
        self.game_board.block_heap.set_full_rows(rows)
 
    def adjust_rows(self,full_rows):
        """removes full rows from block heap"""
        self.game_board.block_heap.adjust_rows(full_rows)

    def print(self):
        """this function prints the entire screen, to the terminal"""
        self.clear()    #clear screen
        #loop through the x,and y coords on screen and print each object on screen
        for y in range(Dim.SCREEN_H,-1,-1):
            for x in range(0,Dim.SCREEN_W):
                print(self[x,y],end = ' ')  #print object at [x,y] coord
            print()
        print(Text.INSTRUCTIONS)    #print game intructions at bottom


    def clear(self):
        """this function clears the terminal screen"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


