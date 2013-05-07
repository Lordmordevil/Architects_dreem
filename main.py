import pygame

import settings
from vec2d import vec2d
from player import Player
from enemies.enemy import EnemyManager
from enemies.zombie import Zombie
from utils import update_focus
from map import Map
from projectiles import fire_bullets


class Game:
    focus = vec2d(0, 0)
    input_list = {
        settings.KEYS['W']: 0,
        settings.KEYS['A']: 0,
        settings.KEYS['S']: 0,
        settings.KEYS['D']: 0
    }
    mouse_pos = vec2d(0, 0)
    bullets = []
    items = []
    world_map = Map()
    zombies = EnemyManager(Zombie, world_map)
    running = False
    clock = pygame.time.Clock()
    fps = 0
    player = Player()

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)
        self.screen.fill(settings.BACKGROUND_COLOR)
        pygame.display.flip()

    def handle_events(self):
        event_types = {
            2: self.key_down,
            3: self.key_up,
            4: self.mouse_motion,
            6: self.mouse_button_up,
            12: self.quit,
        }

        for event in pygame.event.get():
            event_types.get(event.type, lambda s: s)(event)

    def main(self, fps=0):
        self.running = True
        self.fps = fps

        while self.running:
            pygame.display.set_caption("FPS: %i" % self.clock.get_fps())
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def update(self):
        self.player.update(self.input_list, self.items, self.world_map)

        if self.player.health == 0:
            self.running = False

        update_focus(self.player.pos - self.focus, self.focus, self.world_map)
        dead_bullet = None

        for bullet in self.bullets:
            if bullet.life > 0:
                bullet.update(self.zombies.npc_list)
            else:
                dead_bullet = bullet
        if dead_bullet:
            self.bullets.remove(dead_bullet)
        self.zombies.update(self.player, self.items, self.world_map)

    def key_up(self, event):
        if event.key in [settings.KEYS['W'], settings.KEYS['A'], settings.KEYS['S'], settings.KEYS['D']]:
            self.input_list[event.key] = 0

    def key_down(self, event):
        if event.key in [settings.KEYS['W'], settings.KEYS['A'], settings.KEYS['S'], settings.KEYS['D']]:
            self.input_list[event.key] = 1

        if event.key == settings.KEYS['R']:
            self.player.reload()
        if event.key - 48 in range(9):
            self.player.equipped_gun = event.key - 48

    def mouse_button_up(self, event):
        if event.button == 1:
            bullet_dir = vec2d(self.player.pos - self.focus - vec2d(*event.pos) + self.player.direction)
            fire_bullets(self.player, self.bullets, bullet_dir)
        if event.button == 3:
            self.player.reload()

    def mouse_motion(self, event):
        self.mouse_pos = vec2d(event.pos)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.world_map.draw(self.screen, self.focus, self.player.pos)

        for item in self.items:
            item.draw(self.screen, self.focus, self.world_map)

        self.zombies.draw(self.screen, self.focus, self.world_map)

        self.player.draw(self.screen, self.mouse_pos, self.focus)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.focus)

        self.world_map.reset()

    def quit(self, event):
        self.running = False

s = Game()
s.main(60)
