"""
this file contains constant settings for the game, and constants that are used across classes
"""
from getkey import keys

class Text:
    """text displayed for the game"""
    INSTRUCTIONS = 'LEFT: Press a\nRIGHT: Press d\nROTATE: Press w\nDROP BLOCK: Press s\nEXIT GAME: Press q\n'
    NEXT_BLOCK = 'Next: '
    SCORE = 'Score: '
    LEVEL = 'Level: '
    WELCOME_MESSAGE = 'Welcome to tetris'
    STARTING_PROMPT = 'Press p to play, or q to exit:'
    BAD_INPUT = 'Bad input!'
    GAME_OVER = 'GAME OVER!'

class Game_settings:
    """game settings, controlling the gasme speed and scoring"""
    SPEED_MULTIPLIER = .2
    STARTING_SPEED = .5
    LEVEL_SPACING = 5

class Dim:
    """constants setting the diminsions of elements on screen"""
    BOARD_W = 10    #game board is 10x20 blocks
    BOARD_H = 20

    SCREEN_W = 21   #screen diminsions
    SCREEN_H = 21

class Symbols:
    """constants indicating the symbols used to represent objects on screen"""
    SQUARE = '#'
    L = '@'
    J = '+'
    LINE = '='
    T = '%'
    S = 'o'
    Z = '*'
    BLANK = ' '
    BOARDER = '#'
    BOX = '*'
    FULL_ROW = '~'

class Scoring:
    """dictionary used to indicate scoring"""
    POINTS = {
        0:0,
        1:40,
        2:100,
        3:300,
        4:1200}

class Shape_coords:
    """shape descriptions are lists of [x,y] coords"""
    SQUARE = [[0,0],[0,1],[1,1],[1,0]]
    L = [[0,0],[0,1],[0,-1],[1,-1]]
    J = [[0,0],[0,1],[0,-1],[-1,-1]]
    LINE_HORIZONTAL = [[0,0],[-1,0],[1,0],[2,0]]
    LINE_VERTICAL = [[1,0],[1,-1],[1,1],[1,2]]
    T = [[0,0],[0,1],[1,0],[-1,0]]
    S = [[0,0],[0,1],[1,1],[-1,0]]
    Z = [[0,0],[0,1],[-1,1],[1,0]]

class Movement:
    """constants used for movement"""
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
    ROTATE = 'rotate'

    MOVES = {
        DOWN:[0,-1],
        LEFT:[-1,0],
        RIGHT:[1,0]
    }

class Input:
    """constants to check user input against"""
    PLAY = ['p','P']
    QUIT = ['q','Q']
    ROTATE = ['w',keys.UP]
    LEFT = ['a',keys.LEFT]
    RIGHT = ['d',keys.RIGHT]
    DROP = ['s',keys.DOWN]
    
class Exceptions:
    """gameover exception, thrown when the game has been lost"""
    class GameOver(BaseException): pass
