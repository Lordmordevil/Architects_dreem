from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

class Zombie():
    health = 200
    pos = vec2d(100, 100)
    direction = vec2d(0, 0)

    def __init__(self, pos):
        self.pos = vec2d(pos)

    def update(self, player):
        self.direction = player.pos - self.pos
        if self.direction.length > 5:
            self.direction.length = 2
            self.pos += self.direction  

    def draw(self, screen, focus):
        pygame.draw.circle(screen, (250 - self.health//3, 50 + self.health//3, 0), 
                        (int(self.pos[0]) - focus[0], int(self.pos[1]) - focus[1]), 
                        10)
