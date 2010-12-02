from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MIN_SIZE, MAX_SIZE, PLAY_BG, RESIZE_BG, DIRECTION_DICT, DIRECTION_COUNT
import block, grid, display

import pygame, sys, random
from pygame.locals import *

pygame.font.init()

def load_grid():
    try:
        f = open('config', 'r')
        size = f.readline().split()
        
        dim = (int(size[0]), int(size[1]))
        
        dir_map = []
        lines = f.readlines()
        
        for line in lines:
            row = []
            for blk_desc in line.split():
                dirs = [False, False, False, False]
                for c in blk_desc:
                    dirs[int(c)] = True
                row.append(dirs)
            dir_map.append(row)
            
        return (dim, dir_map)
        
    except (IOError, IndexError), e:
        print e
        return ((5, 5), None)

def save_grid(world):
    try:
        f = open('config', 'w')
        f.write(str(world.width) + " " + str(world.height)+"\n")
        
        for row in world.grid:
            for blk in row:
                for d in range(DIRECTION_COUNT):
                    if blk.directions[d]: f.write(str(d))
                f.write(' ')
            f.write('\n')
            
        f.close()
    except IOError, error: print error
    
def draw_message(text, surf, size=50, color=(255, 0, 0)):
    font = pygame.font.Font(None, size)
    text_surf = font.render(text, True, color, (0, 0, 0))
    x = SCREEN_WIDTH/2-text_surf.get_width()/2
    y = SCREEN_HEIGHT/2-text_surf.get_height()/2
    
    updates = []
    updates.append(surf.blit(text_surf, (x,y)))
    
    updates.append(pygame.draw.rect(surf, (255, 0, 0), (x-20, y-20, text_surf.get_width()+30, text_surf.get_height()+30), 10))
    
    return updates

class Game:
    def __init__(self):
        self.state = 'play'
        self.world = None
        self.screen = None
        self.padding = (0, 0)
        
    def resolve_click(self, pt):
        return ((pt[0]-self.padding[0])/display.size[0], (pt[1]-self.padding[1])/display.size[1])
            
    def handle_resize(self, event):
        if event.type != KEYDOWN: return
        
        if event.key == K_RIGHT:
            if self.w >= MAX_SIZE[0]:return
            self.w += 1
            
        elif event.key == K_LEFT:
            if self.w == MIN_SIZE[0]:return
            self.w -= 1
            
        elif event.key == K_UP:
            if self.h == MIN_SIZE[1]:return
            self.h -= 1
            
        elif event.key == K_DOWN:
            if self.h >= MAX_SIZE[1]:return
            self.h += 1
            
        self.init_grid()
        
    def handle_event(self, event):
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            save_grid(self.world)
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN and event.key == K_r:
            self.state = (self.state == 'play') and 'resize' or 'play'
            
        elif self.state == 'resize':
            self.handle_resize(event)

        elif event.type == KEYDOWN and event.key == K_s:
            self.init_grid()
            
        elif event.type == MOUSEBUTTONDOWN:
            self.world.turn_cell(*self.resolve_click(pygame.mouse.get_pos()))
            
            
    def first_play(self):        
        save_data = load_grid()
        self.w, self.h = save_data[0]
        self.init_grid()
        if save_data[1]:
            for i, row in enumerate(save_data[1]):
                for j, dirs in enumerate(row):
                    self.world.grid[i][j].directions = dirs
            self.world.clear_lights()
            
    def init_grid(self):
        
        self.world = grid.Grid(self.w, self.h, self)
        self.world.scramble()
        
        
        self.screen = pygame.display.get_surface()
        if not display.init_images(self.w, self.h, self.screen):
            print "ERROR: Size TOO BIG"
            pygame.quit()
            sys.exit(1)
                        
        self.padding = ( (SCREEN_WIDTH-self.w*display.size[0])/2, (SCREEN_HEIGHT-self.h*display.size[1])/2 )
        
        if self.screen:
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
            
        
            
    def won(self):
        self.state = 'won'
        
    def run(self):        
        pygame.init()

        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Pypes')
        
        pygame.mouse.set_visible(1)
        
        self.first_play()

        while 1:
            for event in pygame.event.get():
                self.handle_event(event)
            
            updates = []
            
            updates.append(pygame.draw.rect(self.screen, self.state == 'resize' and RESIZE_BG or PLAY_BG, (self.padding[0]-5, self.padding[1]-5, self.world.width*display.size[0]+10, self.world.height*display.size[1]+10), 10))
            
            updates.extend(self.world.display(self.screen, self.padding))
            
            
            if self.state == 'won':
                updates.extend(draw_message("You Won!", self.screen))
                        
            pygame.display.update(updates)            
            
            if self.state == 'won':
                self.state = 'play'
                pygame.time.delay(2000)
                self.init_grid()

if __name__ == '__main__':
    Game().run()
