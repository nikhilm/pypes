import random, copy, pprint

import pygame
from pygame.locals import *

from constants import DIRECTION_DICT, DELTAS, OPPOSITES, DIRECTION_COUNT

import block, display

class Grid:
    def __init__(self, width, height, game):
        self.width = width
        self.height = height
        self.game = game
        self.init_empty()
        self.generate()

    def __is_corner(self, x, y):
        return (x == 0 or x == self.width-1) and (y == 0 or y == self.height-1)

    def __is_edge(self, x, y):
        return (x == 0 or x == self.width-1) or (y == 0 or y == self.height-1)

    def __legal_position(self, x, y):
        return ( 0 <= x < self.width ) and ( 0 <= y < self.height )

    def init_empty(self):
        self.grid = []
        for i in range(self.height):
            self.grid.append([])
            for j in range(self.width):
                self.grid[i].append(block.Block(j, i))
                
        # neighbour assignment
        for row in self.grid:
            for b in row:
                for i, (dx, dy) in enumerate(DELTAS):
                    if self.__legal_position(b.x+dx, b.y+dy):
                        b.neighbours[i] = self.grid[b.y+dy][b.x+dx]
                
    def should_i_connect(self, cx, cy, exclude):
        """analyses the block in that direction and returns True or False.
        The decision in made this way:
        The block is checked in each direction ( except *exclude* )
          IF all neighbours are LIT: False
          IF all/few neighbours are DISCONNECTED: True/False (random)
          IF no neighbours disconnected : True
        """
        if not self.__legal_position(cx, cy): return False
        
        current_block = self.grid[cy][cx]
        #print "should_i_connect: current_block %s"%current_block
        #print "EXCLUDING: %s"%DIRECTION_DICT[exclude]
        if current_block.trapped(exclude):
            #print "should_i_connect: current_block is TRAPPED. Returning TRUE"
            return True
        
        all_lit = True            
        all_disconnected = True
        # if someone else already connected then false
        for di in range(DIRECTION_COUNT):
            if di != exclude:
                #print "Direction: %s"%DIRECTION_DICT[di]
                if current_block.neighbours[di] and not current_block.neighbours[di].lit:
                    all_lit = False
                    
                if current_block.neighbours[di] and not current_block.neighbours[di].disconnected():
                    all_disconnected = False
        
        if all_lit:
            #print "All were LIT Returnig FALSE\n--------------"
            return False
        
        if all_disconnected: return True
        #print 'should_i_connect returning %s\n--------'%ch
        return False

    def generate_block(self, x, y):
        '''generates a random block taking into consideration
        any constraints generated due to its position and the
        status of its neighbours'''
        
        if self.lit_count() > 0 and self.grid[y][x].disconnected(): return
        
        if not self.grid[y][x].lit:        
            self.grid[y][x].lit = True
        
        #print "-"*10
        #print "For Block %d, %d"%(x, y)
        for d in range(DIRECTION_COUNT):
            if not self.grid[y][x].directions[d]:
                self.grid[y][x].directions[d] = self.should_i_connect(x+DELTAS[d][0], y+DELTAS[d][1], OPPOSITES[d])
                if self.grid[y][x].directions[d]:
                    self.grid[y][x].neighbours[d].connect(OPPOSITES[d])
                
        for di, (dx, dy) in enumerate(DELTAS):
            if self.grid[y][x].directions[di]:
                self.grid[y+dy][x+dx].directions[OPPOSITES[di]] = True
    
    def turn_cell(self, x, y):
        if not self.__legal_position(x, y): return
        self.grid[y][x].rotate_CW()
        self.clear_lights()
        
        if self.lit_count() == self.width*self.height:
            self.game.won()
        
    def lit_count(self):
        c = 0
        for row in self.grid:
            for b in row:
                if b.lit: c += 1
                
        return c
        
    def clear_lights(self):
        for row in self.grid:
            for b in row:
                b.lit = False
                
        self.grid[self.height/2][self.width/2].light()
        
    def scramble(self):
        for row in self.grid:
            for b in row:
                b.scramble()
        
        self.clear_lights()
        
    def generate(self):
        start_x = random.randint(0, self.width-1)
        start_y = random.randint(0, self.height-1)
        
        #print "-----\nStart %d, %d\n-----"%(start_x, start_y)

        self.generate_block(start_x, start_y)
        
        while self.lit_count() != self.width*self.height:            
            self.generate_block(random.randint(0, self.width-1), random.randint(0, self.height-1))
        

        #pprint.pprint(self.grid, width=120)
       
    def display(self, screen, padding):
        updates = []
        for row in self.grid:
            for block in row:
                surf, pt = display.get_image(block, padding)
                updates.append(screen.blit(surf, pt))
        return updates

if __name__ == '__main__':
    g = Grid(2, 2)
