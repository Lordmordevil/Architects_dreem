import pygame

from random import uniform
from vec2d import vec2d
from items import Item
from utils import collider, wall_collider


class EnemyManager:
    npc_type = None
    npc_list = []

    def __init__(self, npc_type, world_map):
        self.npc_type = npc_type
        for number in range(6):
            self.add(world_map)

    def add(self, world_map):
        self.npc_list.append(self.npc_type(
            vec2d(
                int(uniform(210, 560)) + 100,
                int(uniform(210, 560) + 100)),
            world_map))

    def update(self, player, items, world_map):
        dead_enemy = None
        for enemy in self.npc_list:
            if enemy.health > 0:
                enemy.update(player, world_map)
            else:
                dead_enemy = enemy

        if dead_enemy:
            item_id = int(uniform(1, 3))
            if item_id - 1 in range(2):
                items.append(Item(dead_enemy.pos, item_id))

            world_map.data[dead_enemy.home_cell].entitys.remove(dead_enemy)
            self.npc_list.remove(dead_enemy)
            self.add(world_map)


class Enemy:
    npc_type = ''
    model = ''
    health = 0
    max_health = 0
    size = 0
    pos = vec2d(0, 0)
    direction = vec2d(0, 0)

    def __init__(self, pos, world_map):
        self.pos = vec2d(*pos)
        self.sprite = pygame.image.load(self.model)
        self.base_sprite = self.sprite
        self.home_cell = '{0[0]},{0[1]}'.format([int(pos[0] // CELL_SIZE) + 1, int(pos[1] // CELL_SIZE) + 1])
        world_map.data[self.home_cell].entitys.append(self)

    def draw(self, screen, focus, world_map):
        entity_map_pos = [self.pos[0] // CELL_SIZE, self.pos[1] // CELL_SIZE]
        coords = [int(entity_map_pos[0]), int(entity_map_pos[1])]
        key = '{0[0]},{0[1]}'.format(coords)

        if world_map.data[key].active_light_level > 0:
            screen_pos = vec2d(int(self.pos[0] - focus[0]), int(self.pos[1] - focus[1]))
            self.draw_health(screen, screen_pos)

            rotation = -self.direction
            self.sprite = pygame.transform.rotate(self.base_sprite, int(270 - rotation.get_angle()))
            sprite_size = self.sprite.get_size()
            screen.blit(self.sprite,
                        (int(screen_pos[0] - sprite_size[0] // 2),
                         int(screen_pos[1] - sprite_size[1] // 2)),
                        special_flags=pygame.BLEND_MULT)

    def draw_health(self, screen, screen_pos):
        pygame.draw.line(screen, (0, 0, 0), screen_pos, (screen_pos[0] + 15, screen_pos[1] - 10))
        pygame.draw.rect(screen,
                            (255, 70, 70),
                            (screen_pos[0] + 15,
                            screen_pos[1] + 9,
                            4,
                            int((-1) * self.health / (self.max_health / 18))))
        pygame.draw.rect(screen, (0, 0, 0), (screen_pos[0] + 15, screen_pos[1] - 10, 4, 20), 1)


    def update(self, player, world_map):
        dist = player.pos.get_distance(self.pos)
        if dist < 400:
            self.direction = player.pos - self.pos
            self.direction.length = self.speed
            self.pos += self.direction
            new_home_cell = '{0[0]},{0[1]}'.format([int(self.pos[0] // CELL_SIZE) + 1, int(self.pos[1] // CELL_SIZE) + 1])
            if not new_home_cell == self.home_cell:
                world_map.data[self.home_cell].entitys.remove(self)
                world_map.data[new_home_cell].entitys.append(self)
                self.home_cell = new_home_cell

        collider(self, world_map, self.size, self.npc_type)
        wall_collider(self, world_map, self.size)
