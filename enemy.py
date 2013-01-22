from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

class Zombie_manager():

    zombies = []

    def __init__(self):
        for number in range(10):
            temp = Zombie(vec2d(700, 20 * number))
            self.zombies.append(temp)

    def update(self, player):
        dead_enemy = None
        for enemy in self.zombies:
            if enemy.health > 0:
                enemy.update(player, self.zombies)
            else:
                dead_enemy = enemy
        if not dead_enemy == None:
            self.zombies.remove(dead_enemy)



class Zombie():
    health = 200
    pos = vec2d(100, 100)
    direction = vec2d(0, 0)

    def __init__(self, pos):
        self.pos = vec2d(pos)

    def colider (self, friend):
        dist = self.pos.get_distance(friend.pos)
        if dist < 20:
            overlap = 20 - dist
            ndir = friend.pos - self.pos
            ndir.length = overlap
            ndir.length =  ndir.length / 2
            friend.pos = friend.pos + ndir
            self.pos = self.pos - ndir

    def update(self, player, friends):
        self.direction = player.pos - self.pos
        if self.direction.length > 5:
            self.direction.length = 2
            self.pos += self.direction  
        for friend in friends:
            if not friend == self:
                self.colider(friend)

    def draw(self, screen, focus):
        pygame.draw.circle(screen, (250 - self.health//3, 50 + self.health//3, 0), 
                        (int(self.pos[0]) - focus[0], int(self.pos[1]) - focus[1]), 
                        10)
