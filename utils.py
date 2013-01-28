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

class Wall():

    sprite_dict = { '1':"wall", '2':"door", '3':"window"}

    size = 25

    def __init__(self, pos, wall_type, direct):    
        self.pos = pos
        self.dir = direct
        self.type = wall_type

        self.sprite = pygame.image.load("assets/obsticles/" + self.sprite_dict[wall_type] + ".png")
        if not direct == "0":
            self.sprite = pygame.transform.rotate(self.sprite, int( 90 * (ord(direct) - 48) ))

    def draw(self, screen, focus):
        screen_pos = vec2d(int(self.pos[0] - focus[0]), int(self.pos[1] - focus[1]))
        sprite_size = self.sprite.get_size()
        screen.blit(self.sprite, (int(screen_pos[0] - sprite_size[0]//2), int(screen_pos[1] - sprite_size[1]//2)))


class Map_cell():
    pos = vec2d(0 ,0)
    static_content = null

    def __init__(self, pos):
        pass

    def map_coords_to_pixels(self, coords):
        return vec2d(coordsp[0] * 30 + 15, coordsp[1] * 30 + 15)

    def pixels_to_map_coords(self, coords):
        return vec2d(coords[0]//30, coords[1]//30)

class Map():

    data = []

    def __init__(self):
        map_file = open('assets/map.csv', 'r')
        map_line = map_file.readline()
        coords = [0, 0]
        while not map_line == '':
            cells = map_line.split(";")
            for cell in cells:
                key = '{0[0]},{0[1]}'.format(coords)
                self.data[key] = Map_cell(vec2d(coords[0], coords[1]))
                cell_info = cell.split("/")
                if not cell_info[0] == "0":
                    if cell_info[1] == "0/n":
                        cell_info[1] = "0"
                    self.data[key].static_content = Wall(vec2d(coords[0], coords[1]), cell_info[0], cell_info[1])
                coords[0] += 1


            coords[1] += 1
            coords[0] = 0
            map_line = map_file.readline()

    def define_wall(self, wall):
        pass

    def define_item(self, item):
        pass

    def draw(self, screen, focus):
        pass

    
