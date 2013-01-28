from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

from player import Player
from projectiles import Bullet, fire_bullets
from enemy import Zombie_manager
from debug_tools import debug_static_map
from utils import *
from items import Item



class Starter(PygameHelper):

    focus = vec2d(0, 0)

    input_list = {'W': 0, 'A': 0, 'S': 0, 'D': 0}
    mouse_pos = vec2d(0, 0)

    bullets = []

    items = []

    zombies = Zombie_manager()

    world_map = Map()



    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))

        self.player = Player()
        
    def update(self):
        self.player.update(self.input_list, self.zombies.zombies, self.items, self.buildings.walls)

        
        if self.player.health == 0:
            self.running = False

        update_focus(self.player.pos - self.focus, self.focus)

        dead_bullet = None
        for bullet in self.bullets:
            if bullet.life > 0:
                bullet.update(self.zombies.zombies)
            else:
                dead_bullet = bullet
        if not dead_bullet == None:
            self.bullets.remove(dead_bullet)

        self.zombies.update(self.player, self.items)


    def keyUp(self, key):
        if key == 119:
            self.input_list["W"] = 0
        if key == 97:
            self.input_list["A"] = 0
        if key == 115:
            self.input_list["S"] = 0
        if key == 100:
            self.input_list["D"] = 0
     
    def keyDown(self, key):
        if key == 119:
            self.input_list["W"] = 1
        if key == 97:
            self.input_list["A"] = 1
        if key == 115:
            self.input_list["S"] = 1
        if key == 100:
            self.input_list["D"] = 1
        if key == 114:
            self.player.reload()
        if key - 48 in range(9):
            self.player.equipped_gun = key - 48
        
    def mouseUp(self, button, pos):
        if button == 1:
            bullet_dir = vec2d(self.player.pos - self.focus - vec2d(pos) + self.player.direction)
            fire_bullets(self.player, self.bullets, bullet_dir) 
        if button == 3:
            self.player.reload()
        
    def mouseMotion(self, buttons, pos, rel):
        self.mouse_pos = vec2d(pos)
     

    def draw(self):
        self.screen.fill((255, 255, 255))

        debug_static_map(self.screen, self.focus, self.w, self.h)

        for item in self.items:
            item.draw(self.screen, self.focus)

        for enemy in self.zombies.zombies:
            enemy.draw(self.screen, self.focus)

        self.player.draw(self.screen, self.mouse_pos, self.focus)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.focus)

        self.world_map.draw(self.screen, self.focus)


        
s = Starter()
s.mainLoop(60)
