import pygame
from vec2d import vec2d

from utils import collider, wall_collider
from settings import KEYS


class Player:
    pos = vec2d(400, 300)
    direction = vec2d(0, 0)
    size = 20

    health = 1000
    max_health = 1000

    equipped_gun = 1
    clips = 10
    ammo = 10

    def __init__(self):
        self.hud = pygame.image.load("assets/player/hud.png")
        self.sprite = pygame.image.load("assets/player/player.png")
        self.base_sprite = self.sprite

    def reload(self):
        if self.clips >= 1:
            self.clips -= 1
            self.ammo = 10

    def update_direction(self, input_list):
        self.direction = vec2d(0, 0)

        if input_list[KEYS['W']]:
            self.direction[1] -= 1
        if input_list[KEYS['A']]:
            self.direction[0] -= 1
        if input_list[KEYS['S']]:
            self.direction[1] += 1
        if input_list[KEYS['D']]:
            self.direction[0] += 1

    def update(self, input_list, items, world_map):
        self.update_direction(input_list)

        if self.direction.get_length() and self.health > 0:
            self.direction.length = 2
            self.pos += self.direction

        collider(self, world_map, self.size, "player")

        for item in items:
            dist = self.pos.get_distance(item.pos)
            if dist < 20:
                item.take(self)
                items.remove(item)
        wall_collider(self, world_map, self.size)

    def draw(self, screen, mouse_pos, focus):
        screen_pos = vec2d(int(self.pos[0] - focus[0]), int(self.pos[1] - focus[1]))
        #screen.blit(self.hud, (int(screen_pos[0] - 49), int(screen_pos[1] - 49)))

        pygame.draw.rect(screen,
                         (120, 120, 255),
                         (screen_pos[0] + 25,
                          screen_pos[1] + 9,
                          4,
                          int((-1) * self.ammo / (10 / 18))))
        pygame.draw.rect(screen, (0, 0, 0), (screen_pos[0] + 25, screen_pos[1] - 10, 4, 20), 1)

        for clip in range(self.clips):
            pygame.draw.line(screen, (0, 0, 1),
                             (screen_pos[0] + 35, screen_pos[1] - 10 + clip * 2),
                             (screen_pos[0] + 40, screen_pos[1] - 10 + clip * 2),
                             1)

        pygame.draw.rect(screen,
                         (0, 255, 0),
                         (screen_pos[0] - 25,
                          screen_pos[1] + 9,
                          4,
                          int((-1) * self.health / (self.max_health / 18))))
        pygame.draw.rect(screen, (0, 0, 0), (screen_pos[0] - 25, screen_pos[1] - 10, 4, 20), 1)

        gun_dir = self.pos - focus - mouse_pos
        self.sprite = pygame.transform.rotate(self.base_sprite, int(-90 - gun_dir.get_angle()))
        sprite_size = self.sprite.get_size()
        screen.blit(self.sprite,
                    (int(screen_pos[0] - sprite_size[0] // 2),
                     int(screen_pos[1] - sprite_size[1] // 2)))
