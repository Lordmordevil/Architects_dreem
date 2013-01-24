from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

def colider (obekt, friend, size):
    dist = obekt.pos.get_distance(friend.pos)
    if dist < size:
        overlap = size - dist
        ndir = friend.pos - obekt.pos
        ndir.length = overlap
        ndir.length =  ndir.length / 2
        friend.pos = friend.pos + ndir
        obekt.pos = obekt.pos - ndir

def wall_colider (obekt, wall, size):
    passable = ["2"]
    if not wall.type in passable:
        dist = obekt.pos.get_distance(wall.pos)
        if dist < size:
            overlap = int(size) - dist
            ndir = wall.pos - obekt.pos
            ndir.length = overlap
            obekt.pos = obekt.pos - ndir

def update_focus(alt_player_pos, focus):
    if alt_player_pos[0] > 500:
        focus[0] += alt_player_pos[0] - 500
    if alt_player_pos[1] > 350:
        focus[1] += alt_player_pos[1] - 350
    if alt_player_pos[0] < 300:
        focus[0] -= 300 - alt_player_pos[0]
    if alt_player_pos[1] < 250:
        focus[1] -= 250 - alt_player_pos[1]