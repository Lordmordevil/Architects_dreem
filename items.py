import pygame

from vec2d import vec2d
from settings import CELL_SIZE



class Item():
    pos = vec2d(0, 0)
    tip = 1

    item_id = {1: "clip", 2: "medpack"}

    def __init__(self, pos, tip):
        self.pos = vec2d(pos)
        self.tip = tip
        self.sprite = pygame.image.load("assets/items/" + self.item_id[tip] + ".png")

    def take(self, player):
        if self.tip == 1:
            player.clips += 1
        elif self.tip == 2:
            player.health += 100

    def draw(self, screen, focus, world_map):
        entity_map_pos = [self.pos[0] // CELL_SIZE, self.pos[1] // CELL_SIZE]
        coords = [int(entity_map_pos[0]), int(entity_map_pos[1])]
        key = '{0[0]},{0[1]}'.format(coords)
        if world_map.data[key].active_light_level > 0:
            screen_pos = vec2d(int(self.pos[0] - focus[0]), int(self.pos[1] - focus[1]))
            sprite_size = self.sprite.get_size()
            screen.blit(self.sprite,
                        (int(screen_pos[0] - sprite_size[0] // 2),
                         int(screen_pos[1] - sprite_size[1] // 2)),
                        special_flags=pygame.BLEND_MULT)
