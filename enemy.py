from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

from utils import colider
from items import Item


class Zombie_manager():

    zombies = []

    dead_counter = 0

    def __init__(self):
        for number in range(6):
            self.add_zombie()

    def add_zombie(self):
        temp = Zombie(vec2d(int(uniform(0, 750)), int(uniform(0, 550))))
        self.zombies.append(temp)

    def update(self, player, items):
        dead_enemy = None
        for enemy in self.zombies:
            if enemy.health > 0:
                enemy.update(player, self.zombies)
            else:
                dead_enemy = enemy
        if not dead_enemy == None:
            item_id = int(uniform(1, 3))
            if item_id - 1 in range(2):
                items.append(Item(dead_enemy.pos, item_id))
            self.zombies.remove(dead_enemy)
            self.dead_counter += 1
            print(self.dead_counter)
            self.add_zombie()

class Zombie():

    health = 200
    max_health = 200
    pos = vec2d(100, 100)
    direction = vec2d(0, 0)

    def __init__(self, pos):
        self.pos = vec2d(pos)
        self.sprite = pygame.image.load("assets/enemy/zombie.png")
        self.base_sprite = self.sprite


    def update(self, player, friends):
        self.direction = player.pos - self.pos
        if self.direction.length > 5:
            self.direction.length = 2
            #self.pos += self.direction  
        for friend in friends:
            if not friend == self:
                colider(self, friend)

    def draw(self, screen, focus):
        screen_pos = vec2d(int(self.pos[0] - focus[0]), int(self.pos[1] - focus[1]))

        pygame.draw.line(screen, (0, 0, 0), screen_pos, (screen_pos[0] + 15, screen_pos[1] - 10))

        pygame.draw.rect(screen, (255, 70, 70), (screen_pos[0] + 15, screen_pos[1] + 9, 4,int((-1) * self.health/(self.max_health/18))))
        pygame.draw.rect(screen, (0, 0, 0), (screen_pos[0] + 15, screen_pos[1] - 10, 4, 20), 1)

        rotation = - self.direction
        self.sprite = pygame.transform.rotate(self.base_sprite, int( 270 - rotation.get_angle()))
        sprite_size = self.sprite.get_size()
        screen.blit(self.sprite, (int(screen_pos[0] - sprite_size[0]//2), int(screen_pos[1] - sprite_size[1]//2)))
