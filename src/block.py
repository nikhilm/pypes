import random

from constants import DIRECTION_DICT, DELTAS, DIRECTION_COUNT, OPPOSITES

class Block(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.lit = False
        self.directions = [False, False, False, False]
        self.neighbours = [None, None, None, None]
        
    def light(self):
        if self.lit: return
        self.lit = True
        for di in range(DIRECTION_COUNT):
            if self.directions[di] and self.neighbours[di] and self.neighbours[di].directions[OPPOSITES[di]]:
                self.neighbours[di].light()

    def readjust_neighbours(self):
        for di in range(DIRECTION_COUNT):
            if self.neighbours[di]:
                self.neighbours[di].directions[OPPOSITES[di]] = self.directions[di]
            
    def rotate_CW(self):
        """rotates self.directions"""
        self.directions.insert(0, self.directions.pop())

    def rotate_ACW(self):
        self.directions.append(a.pop(0))

    def disconnected(self):
        return self.directions == [False]*4
    
    def trapped(self, exclude):
        for di in range(DIRECTION_COUNT):
            if di != exclude and self.neighbours[di] and self.neighbours[di].directions[OPPOSITES[di]]:
                return False
            
        return True
    
    def scramble(self):
        for i in range(random.randint(0, DIRECTION_COUNT)):
            self.rotate_CW()

    def connect(self, direction):
        self.directions[direction] = True

    def __repr__(self):
        dirmap = ''.join([self.directions[i] and 'T' or 'F' for i in range(DIRECTION_COUNT)])
        return "%s|%s (%d,%d)"%(dirmap, self.lit and 'T' or 'F', self.x, self.y)

if __name__ == '__main__':
    b = Block(0, 4)
    b.connect(DOWN, Block(1, 4))
    b.connect(RIGHT, Block(0, 5))
    print b
