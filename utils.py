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