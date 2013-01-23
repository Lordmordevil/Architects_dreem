from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *

class Item():
    pos = vec2d(0, 0)
    tip = 1

    item_id = {1: "clip"}

    def __init__(self, pos, tip):
        self.pos = vec2d(pos)
        self.tip = tip
        self.sprite = pygame.image.load("assets/items/" + self.item_id[tip] + ".png")

    def take(self, player):
        if self.tip == 1:
            player.clips += 1

    def draw(self, screen, focus):
        screen_pos = vec2d(int(self.pos[0] - focus[0]), int(self.pos[1] - focus[1]))
        sprite_size = self.sprite.get_size()
        screen.blit(self.sprite, (int(screen_pos[0] - sprite_size[0]//2), int(screen_pos[1] - sprite_size[1]//2)))