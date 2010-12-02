import sys
import pygame
import pygame.image

from constants import DIRECTION_COUNT, BLOCK_SIZES, SCREEN_WIDTH, SCREEN_HEIGHT
import block

def get_size(gwidth, gheight):
    sizes = BLOCK_SIZES.keys()
    sizes.sort()
    sizes.reverse()

    for size in sizes:
        if gwidth * size[0] < SCREEN_WIDTH and gheight * size[1] < SCREEN_HEIGHT:
            return (size, BLOCK_SIZES[size])

    return ((0, 0), False)

def get_block_value(block):
    value = 0
    for i, di in enumerate(block.directions):
        if di:
            value += 2**i

    return (value, block.lit and 1 or 0)

def init_images(gwidth, gheight, screen_surf):
    global size, tiles, image_cache
    size, name = get_size(gwidth, gheight)
    if not name: return name
    tiles = pygame.image.load('../images/%s.png'%name).convert(screen_surf)
    image_cache = {}
    return True

def get_image(block, padding):
    """returns a (clipped surface, its top left corner)"""
    val = get_block_value(block)
    if not image_cache.has_key(val):
        image_cache[val] = tiles.subsurface(( val[0]*size[0], val[1]*size[1], size[0], size[1]))

    return (image_cache[val], (padding[0]+block.x*size[0], padding[1]+block.y*size[1]))

#print get_size(int(sys.argv[1]), int(sys.argv[2]))
