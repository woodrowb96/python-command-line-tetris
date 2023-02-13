"""
this file contains the game class, which is used to describe a complete tetris game
    
this class uses the getkeys package to get user input
"""
from Screen import Screen
from Shape import J,L,T,Line,Square,S,Z
from Settings import Text,Exceptions,Game_settings,Scoring,Input,Movement

import random
import os
import threading
import time
import math
from getkey import getkey, keys #getkey package used to get user input
    
class Game():
    """
    the Game class describes the tetris game
    
    a game is described by the following
    screen: the games screen with all objects used to play the game on it
    score,level: the games current score and level
    total_lines_cleared: total lines that have been cleared by the player, used to calculate the current level
    game_speed: the time that one turn takes, used to set the speed of the game
    game_active: true if the game is being played, false if it is over 
    """
 
    def __init__(self):
        self.screen = Screen()
        self.score = 0
        self.level = 0
        self.total_lines_cleared = 0
        self.game_speed = Game_settings.STARTING_SPEED
        self.game_active = True

    def start(self): 
        """this function prompts the user if they want to play or not, if they do it returns true, else false"""
        self.screen.clear() 
        print(Text.WELCOME_MESSAGE)
        while(True):
            choice = input(Text.STARTING_PROMPT)
            if choice in Input.PLAY:
                return True
            elif choice in Input.QUIT:
                return False            
            print(Text.BAD_INPUT) #if choice was not in PLAY or QUIT it was bad input, reprompt the user
 
    def play(self):
        """
            this function is used to play the game
            it starts the thread that accepts user input,
            it executes turn() funciton until the game is lost or has been exited by the user
            returns false when the game is over
        """  

        th = threading.Thread(target = self.get_input)  #thread to get user input
        th.start() 
        while self.game_active: #game_active can be unset by the user, to stop playing the game
            try:
                self.turn() #do a turn
            except Exceptions.GameOver: #until the game has been lost
                self.game_active = False    #end the game
                th.join()   #wait for the user input thread to join
                
        print(Text.GAME_OVER)
        return False
            
 
    def turn(self):
        """this fucntions executes a single turn of the game"""

        self.screen.move_block(Movement.DOWN)   #move the block down
        self.screen.print() 

        full_rows = self.screen.get_full_rows() #check if there are any full rows
        self.screen.set_full_rows(full_rows)
        
        self.screen.score = self.update_score(len(full_rows))   #update the level and score based num of full_rows
        self.screen.level = self.update_level(len(full_rows))
        time.sleep(self.game_speed*.1)  #sleep and update the screen
        self.screen.print()
        
        self.screen.adjust_rows(full_rows)  #remove the rows
        time.sleep(self.game_speed*.9)  #sleep for the remaining turn time

    def update_score(self,rows_cleared):
        """this function updates the score,based on the level ,and how many rows were cleared that turn"""
        #the score multiplier depends on how many rows were cleared
        multiplier = Scoring.POINTS[rows_cleared] 
        #the added score is calulated as new_score = multiplier x (level + 1)
        self.score += multiplier*(self.level+1)
        return self.score 

    def update_level(self,rows_cleared):
        self.total_lines_cleared += rows_cleared 
        
        #total_lines_cleared - level x level_spacing, should be greater than level_spacing if we are 
        #to move on to the next level
        if self.total_lines_cleared - self.level*Game_settings.LEVEL_SPACING >= Game_settings.LEVEL_SPACING:
            self.level += 1     #increment level and
            self.update_speed() #update the speed
        return self.level

    def update_speed(self):
        #update speed according to equation 
        #speed = start_speed x e^(-speed_multiplier x level)
        #this equation probably should be adjusted or changed to later to have the game play the best
        self.game_speed = Game_settings.STARTING_SPEED * math.exp(-Game_settings.SPEED_MULTIPLIER*self.level)
 
    def print_game(self):
        self.board.print_board()

    def get_input(self):
        """
            this function should run as a thread in the background and get input from the player
            this function uses the getkey package to get one key input from the user with no enter required
        """
        while self.game_active:#get input while the game is active
            key = getkey(blocking=False)    #get user input
            #check if inoput mathces any actions to be performed
            if key in Input.ROTATE:
                self.screen.rotate_block() 
            elif key in Input.LEFT:
                self.screen.move_block(Movement.LEFT)
            elif key in Input.RIGHT:
                self.screen.move_block(Movement.RIGHT)
            elif key in Input.DROP:
                self.screen.drop_block()
            elif key in Input.QUIT:
                self.game_active = False    #if we quit the game,set game_active to false
        return  #return from thread when game_active has gone false
