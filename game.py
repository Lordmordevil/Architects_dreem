from pygamehelper import PygameHelper
from vec2d import vec2d

from settings import KEYS
from player import Player
from enemy import Zombie_manager
from utils import update_focus
from map import Map
from projectiles import fire_bullets


class Starter(PygameHelper):
    focus = vec2d(0, 0)
    input_list = {KEYS['W']: 0, KEYS['A']: 0, KEYS['S']: 0, KEYS['D']: 0}
    mouse_pos = vec2d(0, 0)
    bullets = []
    items = []
    world_map = Map()
    zombies = Zombie_manager(world_map)

    def __init__(self):
        self.w, self.h = 800, 600
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255, 255, 255)))
        self.player = Player()

    def update(self):
        print(self.input_list)
        self.player.update(self.input_list, self.zombies.zombies, self.items, self.world_map)

        if self.player.health == 0:
            self.running = False

        update_focus(self.player.pos - self.focus, self.focus, self.world_map)
        dead_bullet = None

        for bullet in self.bullets:
            if bullet.life > 0:
                bullet.update(self.zombies.zombies)
            else:
                dead_bullet = bullet
        if dead_bullet:
            self.bullets.remove(dead_bullet)

        self.zombies.update(self.player, self.items, self.world_map)

    def keyUp(self, key):
        if key in [KEYS['W'], KEYS['A'], KEYS['S'], KEYS['D']]:
            self.input_list[key] = 0

    def keyDown(self, key):
        if key in [KEYS['W'], KEYS['A'], KEYS['S'], KEYS['D']]:
            self.input_list[key] = 1

        if key == KEYS['R']:
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
        self.screen.fill((0, 0, 0))
        self.world_map.draw(self.screen, self.focus, self.player.pos)

        for item in self.items:
            item.draw(self.screen, self.focus, self.world_map)

        for enemy in self.zombies.zombies:
            enemy.draw(self.screen, self.focus, self.world_map)

        self.player.draw(self.screen, self.mouse_pos, self.focus)

        for bullet in self.bullets:
            bullet.draw(self.screen, self.focus)

        self.world_map.reset()


s = Starter()
s.mainLoop(60)
