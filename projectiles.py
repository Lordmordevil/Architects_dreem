from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

class Bullet():

    pos = vec2d(100, 100)
    direction = vec2d(0, 0)
    life = 50

    def __init__(self, pos, direction):
        self.pos = vec2d(pos)
        self.direction = vec2d(0, 0) - direction
        self.direction.length = 6

    def update(self, enemys):
        self.life -= 1
        if self.life > 0:
            self.pos += self.direction
        for enemy in enemys:
            dist = self.pos - enemy.pos
            if dist.length < 30:
                self.life = 0
                enemy.health -= 30

    def draw(self, screen, focus):
        pygame.draw.line( screen, (150, 0, 0), 
                        (int(self.pos[0]) - focus[0], int(self.pos[1]) - focus[1]), 
                        (int(self.pos[0] - self.direction[0]) - focus[0], int(self.pos[1] - self.direction[1]) - focus[1]), 2)