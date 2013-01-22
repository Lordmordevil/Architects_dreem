from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

from player import Player
from projectiles import Bullet
from enemy import Zombie

def debug_static_map(screen, focus, screen_width, screen_height):
        def draw_colmn(x_pos, height, screen):
            for lines in range((height // 10)):
                pygame.draw.line(screen, (220, 220, 220), (x_pos, lines * 10), (x_pos, (lines * 10) + 5)) 

        def draw_row(y_pos, height, screen):
            for lines in range((height // 10)):
                pygame.draw.line(screen, (220, 220, 220), (lines * 10, y_pos), ((lines * 10) + 5, y_pos))

        box_size = 30
        offset = vec2d(0, 0)
        offset[0] = focus[0] % box_size
        offset[1] = focus[1] % box_size
        width_line_count = screen_width//box_size
        height_line_count = screen_height//box_size
        for colmn in range(width_line_count + 1):
            draw_colmn(offset[0] + colmn * box_size, screen_height, screen)
        for row in range(height_line_count + 1):
            draw_row(offset[1] + row * box_size, screen_width, screen)

class Starter(PygameHelper):

    focus = vec2d(0, 0)

    input_list = {'W': 0, 'A': 0, 'S': 0, 'D': 0}
    mouse_pos = vec2d(0, 0)

    bullets = []
    enemys = []

    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))

        self.player = Player()

        for number in range(10):
            temp = Zombie(vec2d(700, 20 * number))
            self.enemys.append(temp)
        
    def update(self):
        self.player.update(self.input_list)

        dead_bullet = None
        for bullet in self.bullets:
            if bullet.life > 0:
                bullet.update(self.enemys)
            else:
                dead_bullet = bullet
        if not dead_bullet == None:
            self.bullets.remove(dead_bullet)

        dead_enemy = None
        for enemy in self.enemys:
            if enemy.health > 0:
                enemy.update(self.player)
            else:
                dead_enemy = enemy
        if not dead_enemy == None:
            self.enemys.remove(dead_enemy)


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

        
    def mouseUp(self, button, pos):
        temp_bullet = Bullet(self.player.pos, self.player.pos - vec2d(pos) + self.player.direction)
        self.bullets.append(temp_bullet)
        
    def mouseMotion(self, buttons, pos, rel):
        self.mouse_pos = vec2d(pos)
      
    def draw(self):
        self.screen.fill((255, 255, 255))

        debug_static_map(self.screen, self.focus, self.w, self.h)

        self.player.draw(self.screen, self.mouse_pos, self.focus)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.focus)

        for enemy in self.enemys:
            enemy.draw(self.screen, self.focus)

        
s = Starter()
s.mainLoop(40)
