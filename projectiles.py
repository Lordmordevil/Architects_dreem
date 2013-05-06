import pygame

from vec2d import vec2d


def fire_bullets(player, bullets, bullet_dir):
    gun_pos = vec2d(- 15, - 7)
    gun_pos.rotate(bullet_dir.get_angle())
    if player.equipped_gun == 1 and player.ammo >= 1:
        new_bullet = Bullet(player.pos + gun_pos, bullet_dir)
        bullets.append(new_bullet)
        player.ammo -= 1
    elif player.equipped_gun == 2 and player.ammo >= 5:
        for direct in range(5):
            new_bullet = Bullet(player.pos + gun_pos, bullet_dir.rotated(int((direct - 2) * 5)))
            bullets.append(new_bullet)
        player.ammo -= 5
        bullet_dir.length = 6
        player.pos += bullet_dir


class Bullet:
    pos = vec2d(100, 100)
    direction = vec2d(0, 0)
    life = 50

    def __init__(self, pos, direction):
        self.pos = vec2d(pos)
        self.direction = vec2d(0, 0) - direction
        self.direction.length = 6

    def update(self, enemys):
        self.life -= 1
        if self.life > 0:
            self.pos += self.direction
        for enemy in enemys:
            dist = self.pos - enemy.pos
            if dist.length < 10:
                self.life = 0
                enemy.health -= 30
                enemy.pos += self.direction

    def draw(self, screen, focus):
        pygame.draw.line(screen, (150, 0, 0),
                         (int(self.pos[0]) - focus[0],
                          int(self.pos[1]) - focus[1]),
                         (int(self.pos[0] - self.direction[0]) - focus[0],
                          int(self.pos[1] - self.direction[1]) - focus[1]), 2)
