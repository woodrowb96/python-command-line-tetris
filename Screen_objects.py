"""
This file contains classes used to describe objects that can be printed to the screen during
a game of tetris

Those objects the following
    background,box,block,text,block_heap

This file also containts the Multi_object class, which is used to create objects made of multiple screen_objects

The multi_object class is the parent class of the following classes
    Block_box,multi_line_text,game_board
"""
from Settings import Dim,Movement,Exceptions,Symbols

import time
import copy


class Screen_object():
    """
    This is the parent class of all screen objects
    A screen object is described using by the following
        location: objects [x,y] coord on screen
        symbol: symbol printed to screen to represent the object
        description: [x,y] coords independent of location used to describe the object
    """ 

    def __init__(self,location,description = [],symbol = None):
        self.location = location
        self.symbol = symbol
        self._description = description

    def __getitem__(self,coord):
        """
            this function returns the object symbol 
            if the object is at location  coord on the screen 
            else returns None
        """

        #_description is location independent so
        #strip the coord of its location to check if its in _description
        stripped_coord = [coord[0] - self.location[0],coord[1] - self.location[1]]
        if stripped_coord in self._description:
            return self.symbol

    @property
    def description(self):
        """return the objects description relative to its location on hte screen"""
        return [[x + self.location[0],y + self.location[1]] for x,y in self._description] 

class Background(Screen_object):
    """This class describes a square background"""

    def __init__(self,height,width,location,symbol):
        self.location = location 
        self.symbol = symbol
        self._description = []
        
        #description should be each coord inside 
        #the square background 
        for x in range(0,height):
            for y in range(0,width):
                self._description.append([x,y])
 
def gen_box_coords(height,width):
    """ generate the description of a box of height and width"""
    box = []
    for y in range(0,height + 1):
        box.append([0,y])
        box.append([width,y])
    for x in range(0,width + 1):
        box.append([x,0])
        box.append([x,height])
    return box
 
class Box(Screen_object):
    """ this class describes an empty box of height and width""" 
    def __init__(self,height,width,location,symbol):
        self.height = height
        self.width = width
        
        self.location = location
        self._description = gen_box_coords(height,width)
        self.symbol = symbol


class Block(Screen_object):
    """
        this class describes the blocks used on in a tetris game
        
        a block is built from a shape from the Shape class
            
        blocks can be rotated and unrotated
    """

    def __init__(self,shape,location):
        self._shape = shape
        
        self.location = location
        self._description = shape.description
        self.symbol = shape.symbol

    @property
    def shape(self):
        return self._shape
    
    @shape.setter
    def shape(self,shape):
        """when setting a shape, need to update symbol and description"""
        self._shape = shape
        self.symbol = shape.symbol
        self._description = shape.description
   
    def rotate(self):
        self._shape.rotate() 
        self._description = self.shape.description

    def un_rotate(self):
        self._shape.un_rotate()
        self._description = self.shape.description


class Text(Screen_object):
    """this class describes a single line of text on the screen"""
    
    def __init__(self,text,location):
        self._text = text
        
        self.location = location
        #need a coord for each char in the text
        self._description = [[i,0] for i in range(len(text))]

        #texts symbols are the charecters in text
        self.symbol = text

    def __getitem__(self,coord):
        """
        text has it own getitem function, because there are multiple symbols
            used to represent the text on screen
        """  
        stripped_coord = [coord[0] - self.location[0],coord[1] - self.location[1]]
        symbol_index = stripped_coord[0]
        if stripped_coord in self._description:
            return self.symbol[symbol_index]
   
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self,new_text):
        """need to update symbol and description when setting text"""
        
        self._text = new_text
        self.symbol = new_text
        self._description = [[i,0] for i in range(len(new_text))] 

class Block_heap(Screen_object):
    """
    this class describes the games block heap
        
    the block heap is the heap of blocks at the bottom of a tetris game
        that grows and shrinks as the game goes on
    
    the block heap doesnt use the same description or symbol as the other screen_objects
    
    the block heap is described using a list of rows, on the tetris game board
        each element in the row is either a symbol representing the block at that 
        coordinate, or None if there is nothing at that coordinate  
    """  

    def __init__(self,width,location):
        self.width = width #width of the block heap
        self.block_heap = []
        
        self.location = location
        self._description = []
        self.symbol = None
 
    def __setitem__(self,coord,symbol):
        """this function is used to add a symbol to the block heap at the [x,y] coord"""
        x,y = coord[0] - self.location[0],coord[1] - self.location[1]
        #if y is not in the heap, we need to add a new empty row to the heap
        while y >= len(self.block_heap):
            self.block_heap.append(self.empty_row()) 
        #then we can add the symbol to the correct row and column in the heap
        self.block_heap[y][x] = symbol 
                             
    def __getitem__(self,coord):
        """this function returns the symbol at the coord on the screen, or 
           returns none if there is no block_heap located at that coord""" 
        x,y = coord[0] - self.location[0],coord[1] - self.location[1]
        try: 
            return self.block_heap[y][x]
        except IndexError: 
            return None
 
    def get_full_rows(self):
        """this function returns a list of indexes of each full row in the heap"""
        #a row is full if None is not in the row
        return [self.block_heap.index(row) for row in self.block_heap if None not in row]         
    
    def set_full_rows(self,full_rows):
        """this function replaces each full row with a row of symbols representing a full row
            it is used to animate a row being removed"""
        for row in full_rows:
            self.block_heap[row] = self.full_row()

    def adjust_rows(self,removed_rows):
        """this function removes the full rows from the heap"""
        [self.block_heap.pop(row) for row in removed_rows]

    def empty_row(self):
        """this funciton generates an empty row, filled with None"""
        return [None for x in range(0,self.width)]
    
    def full_row(self):
        """this funciton generates a full row"""
        return [Symbols.FULL_ROW for x in range(0,self.width)]



class Multi_object():
    """
    A multi_object has 
        location:objects location on screen
        object: a list of all screen_objects that make up the multi_object
    """
    
    def __init__(self,location):
        self.location = location
        self.objects = []

    def __getitem__(self,coord):
        #loop through all objects until one has a symbol 
        #at coord, then return that symbol
        for obj in self.objects:
            symbol = obj[coord]
            if symbol:
                return symbol

class Block_box(Multi_object):
    """
    this class describes a block_box, a box with a block inside of it
    this is used to display the games next block on the screen
    """
        
    def __init__(self,shape,height,width,label_text,location,box_symbol):
        self.location = location    
    
        #boarder height and width
        self.height = height 
        self.width = width 

        self.boarder_location = location
        self.boarder = Box(height,width,self.boarder_location,box_symbol)
        
        #place block in the middle of the box
        self.block_location = [int(width/2) + location[0],int(height/2) + location[1]]
        self._block = Block(shape,self.block_location)

        #text is located above the box
        text_location = [location[0],location[1] + height + 1]
        self.label = Text(label_text,text_location)

        self.objects = [self.boarder,self.block,self.label]

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self,shape):
        self._block.shape = shape

 
class Multi_line_text(Multi_object):
    """
    this class is used to describe multiple lines of text
    the top line is at index 0,the next lowest one is at index 1,....
    """
        
    def __init__(self,location,text_lines):
        """
            multi_line_text is initialized by passing a list of text_lines
            line at index 0 is placed displayed on top on screen ,index 1 is next,...
        """ 
        
        self.location = location
        self.objects = []
        #give each line a location relative to location, according to its index
        for i,line in enumerate(text_lines):
            line_location = [location[0],location[1] - i]
            self.objects.append(Text(line,line_location))

    def __setitem__(self,line_index,new_text):
        self.objects[line_index].text = new_text  

class Game_board(Multi_object):
    """
        This class describes the playing board where the game is playes
        
        This class contains a:
            Boarder: box displayed around the game board
            Block: falling block that the player controles
            block_heap: the games block heap
    """
    
    def __init__(self,shape,height,width,location,boarder_symbol):
        """at initialization place all objects at the correct place relative to location"""
        self.location = location
        
        self.width = width
        self.height = height
 
        self.boarder_w = width + 1
        self.boarder_h = height + 1
        self.boarder_location = [location[0] - 1,location[1] - 1] 
        self.boarder = Box(self.boarder_h,self.boarder_w,self.boarder_location,boarder_symbol)
      
        self._block_start_location = [int(width/2) + location[0],height + location[1] + 1]
        self._block = Block(shape,self.block_start_location)

        self.block_heap = Block_heap(width,location)
 
        self.objects = [self.boarder,self._block,self.block_heap] 

    @property 
    def block_start_location(self):
        return copy.copy(self._block_start_location)

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self,block):
        """when setting the block, we want it to be placed back at the top of the board"""
        self._block.shape = block.shape
        self._block.location = self.block_start_location
 
    def move_block(self,direction):
        """move the block by changing its location, then check if that was a valid move"""
        self._block.location[1] += Movement.MOVES[direction][1]
        self._block.location[0] += Movement.MOVES[direction][0]
        self.check_move(direction) #check_move will throw exceptions to indicate an invalid move

    def un_move_block(self,direction):
        self._block.location[1] -= Movement.MOVES[direction][1]
        self._block.location[0] -= Movement.MOVES[direction][0]
    
    def rotate_block(self):
        """rotate block then check if the rotation was a valid move"""
        self._block.rotate()
        self.check_move()
    
    def un_rotate_block(self):
        self._block.un_rotate()

    def add_block_to_heap(self):
        board_top = self.boarder_location[1] + self.boarder_h
       
        #loop throught the blocks description and add each coord to the block_heap 
        for x,y in self.block.description:
            if y == board_top:
                raise Exceptions.GameOver
            self.block_heap[[x,y]] = self.block.symbol

    def check_move(self,direction = None):
        """checks if a move was valid,throws an exceptions if
                move was invalid, or 
                block shoulb be added to the block_heap
        """

        board_top = self.boarder_location[1] + self.boarder_h
        board_bottom = self.boarder_location[1]

        #loop throught the blocks description and see is there are any other objects at that coord
        for x,y in self.block.description:
            if y == board_bottom: #add to heap if block is at the bottom of the board
                raise self.AddToHeap
            elif self.block_heap[[x,y]]:    #if there is a conflict with the block_heap
                if direction == Movement.DOWN:  #only add block to heap if it was moving down
                    raise self.AddToHeap
                raise self.InvalidMove      #else move is invalid
            elif self.boarder[[x,y]] and y != board_top:    #any other boarder conflicat and move is invalid
                raise self.InvalidMove    
 
    class InvalidMove(BaseException): pass
    
    class AddToHeap(BaseException): pass 
