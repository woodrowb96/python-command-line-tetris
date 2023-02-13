"""
this file contains classes used to represent the following shapes for a tetris game
    shapes:Square,L,J,Line,T,S,Z
"""
from Settings import Symbols,Shape_coords
import time

import copy


class Shape():
    """
        This class is the parent to all other shape on a tetris board
        Shape have a description used to describe the shape
        Shapes have a symbol that is used to represent the shape on the screen
    """

    def __init__(self):
        #description is as a list of [x,y] coordinantes 
        self._description = []
        self.symbol = None
   
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self,coords):
        """
            I want to copy the coords into the description, when setting it
            not get a reference to those coords
        """ 
        
        #descriptions are lists of lists,so use a deepcopy
        self._description = copy.deepcopy(coords)
 
    def rotate(self):
        #rotations is done using the equations
        #new_y = -old_x 
        #new_x = old_y
        self.description = [[y,-x] for x,y in self.description]
    
    def un_rotate(self):
        #un rotate the shape according to the inverse of the rotation equations
        self.description = [[-y,x] for x,y in self.description]


class Square(Shape):
    
    def __init__(self):
        self.description = Shape_coords.SQUARE
        self.symbol = Symbols.SQUARE

    def rotate(self):
        #square is symetrical, so no rotation needed
        pass
    
    def un_rotate(self):
        pass


class L(Shape):
    
    def __init__(self):
        self.description = Shape_coords.L
        self.symbol = Symbols.L


class J(Shape):
    
    def __init__(self):
        self.description = Shape_coords.J
        self.symbol = Symbols.J


class Line(Shape):
    
    def __init__(self):
        self.description = Shape_coords.LINE_HORIZONTAL
        self.symbol = Symbols.LINE

    def rotate(self):
        #switch line to the opposite position
        if self.description == Shape_coords.LINE_HORIZONTAL:
            self.description = Shape_coords.LINE_VERTICAL
        else:
            self.description = Shape_coords.LINES_HORIZONTAL
         
    def un_rotate(self):
        self.rotate() 


class T(Shape):
    
    def __init__(self):
        self.description = Shape_coords.T
        self.symbol = Symbols.T


class S(Shape):
    
    def __init__(self):
        self.description = Shape_coords.S
        self.symbol = Symbols.S


class Z(Shape):
    
    def __init__(self):
        self.description = Shape_coords.Z 
        self.symbol = Symbols.Z
