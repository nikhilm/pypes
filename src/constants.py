############
#  BLOCKS  #
############
DIRECTION_COUNT = 4
UP, RIGHT, DOWN, LEFT = range(DIRECTION_COUNT)
OPPOSITES = [DOWN, LEFT, UP, RIGHT]

# this is just for programmers, used in Block.__repr__, but good to have here
DIRECTION_DICT = { UP: 'U', DOWN: 'D', LEFT: 'L', RIGHT: 'R' }
# DELTAS are differences for each direction relative to current block
DELTAS = [ (0, -1), (1, 0), (0, 1), (-1, 0) ]


#############
#  DISPLAY  #
#############

BLOCK_SIZES = { (25,25): 'small', (50, 50): 'medium', (75, 75): 'large' }

SCREEN_WIDTH, SCREEN_HEIGHT = (800, 600)

MAX_SIZE = (31, 23)
MIN_SIZE = (2, 2)

PLAY_BG = (0, 0, 255)
RESIZE_BG = (255, 0, 0)