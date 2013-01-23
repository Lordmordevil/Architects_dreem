from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

def colider (obekt, friend):
    dist = obekt.pos.get_distance(friend.pos)
    if dist < 20:
        overlap = 20 - dist
        ndir = friend.pos - obekt.pos
        ndir.length = overlap
        ndir.length =  ndir.length / 2
        friend.pos = friend.pos + ndir
        obekt.pos = obekt.pos - ndir

def update_focus(alt_player_pos, focus):
    if alt_player_pos[0] > 700:
        focus[0] += alt_player_pos[0] - 700
    if alt_player_pos[1] > 500:
        focus[1] += alt_player_pos[1] - 500
    if alt_player_pos[0] < 100:
        focus[0] -= 100 - alt_player_pos[0]
    if alt_player_pos[1] < 100:
        focus[1] -= 100 - alt_player_pos[1]