from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

class Player():

    pos = vec2d(100, 100)
    direction = vec2d(0, 0)

    def __init__(self):
        pass

    def update(self, input_list):
        self.direction = vec2d(0, 0)

        if input_list["W"]:
            self.direction[1] -= 1
        if input_list["A"]:
            self.direction[0] -= 1
        if input_list["S"]:
            self.direction[1] += 1
        if input_list["D"]:
            self.direction[0] += 1
        if self.direction.get_length():
            self.direction.length = 2
            self.pos += self.direction  

    def draw(self, screen, mouse_pos, focus):
        pygame.draw.circle(screen, (0, 0, 0), 
                        (int(self.pos[0]) - focus[0], int(self.pos[1]) - focus[1]), 
                        10)
        gun_dir = self.pos - mouse_pos
        gun_dir.length = 15
        pygame.draw.line( screen, (110, 110, 110), 
                        (int(self.pos[0]) - focus[0], int(self.pos[1]) - focus[1]), 
                        (int(self.pos[0] - gun_dir[0]) - focus[0], int(self.pos[1] - gun_dir[1]) - focus[1]), 2)