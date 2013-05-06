from random import uniform

from vec2d import vec2d
from .enemy import Enemy


class Zombie(Enemy):
    health = 200
    max_health = 200
    pos = vec2d(100, 100)
    speed = 2
    size = 20
    npc_type = 'zombie'
    direction = vec2d(int(uniform(0, 3)) - 1, int(uniform(0, 3) - 1))
    model = "assets/enemy/zombie.png"
