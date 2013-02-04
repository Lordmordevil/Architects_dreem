from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from math import e, pi, cos, sin, sqrt
from random import uniform

def colider (obekt, world_map, size, obekt_type):
    obekt_pos = vec2d(obekt.pos[0]//30, obekt.pos[1]//30)
    for x in range(3):
        for y in range(3):           
            coords = [int(obekt_pos[0]) - 1 + x, int(obekt_pos[1]) - 1 + y] 
            key = '{0[0]},{0[1]}'.format(coords)
            cell = world_map.data[key]
            for friend in cell.entitys:
                if not friend == obekt:
                    dist = obekt.pos.get_distance(friend.pos)
                    if dist < size:
                        overlap = size - dist
                        ndir = friend.pos - obekt.pos
                        ndir.length = overlap
                        ndir.length =  ndir.length / 2
                        friend.pos = friend.pos + ndir
                        obekt.pos = obekt.pos - ndir
                        if obekt_type == "player":
                            if obekt.health < 1:
                                obekt.health = 0
                            else:
                                obekt.health -= 1
                                if friend.health + 1 < friend.max_health:
                                    friend.health +=1

def wall_colider (obekt, world_map, size):
    obekt_pos = vec2d(obekt.pos[0]//30, obekt.pos[1]//30)
    passable = ["2"]
    for x in range(3):
        for y in range(3):           
            coords = [int(obekt_pos[0]) - 1 + x, int(obekt_pos[1]) - 1 + y] 
            key = '{0[0]},{0[1]}'.format(coords)
            cell = world_map.data[key]
            if type(cell.static_content) == Wall and not cell.static_content.type in passable:
                dist = obekt.pos.get_distance(cell.map_coords_to_pixels(cell.static_content.pos))
                if dist < size + 10:
                    overlap = int(size + 10) - dist
                    ndir = cell.map_coords_to_pixels(cell.static_content.pos) - obekt.pos
                    ndir.length = overlap
                    obekt.pos = obekt.pos - ndir

def update_focus(alt_player_pos, focus, world_map):
    if alt_player_pos[0] > 500 and focus[0] < world_map.map_size[0] - 830:
        focus[0] += alt_player_pos[0] - 500
    if alt_player_pos[1] > 350 and focus[1] < world_map.map_size[1] - 630:
        focus[1] += alt_player_pos[1] - 350
    if alt_player_pos[0] < 300 and focus[0] > 30:
        focus[0] -= 300 - alt_player_pos[0]
    if alt_player_pos[1] < 250 and focus[1] > 30:
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
        screen_pos = vec2d(int(self.pos[0] * 30 + 15 - focus[0]), int(self.pos[1] * 30 + 15 - focus[1]))
        sprite_size = self.sprite.get_size()
        screen.blit(self.sprite, (int(screen_pos[0] - sprite_size[0]//2), int(screen_pos[1] - sprite_size[1]//2)))


class Map_cell():
    pos = vec2d(0 ,0)
    static_content = []
    entitys = []

    def __init__(self, pos):
        pass

    def map_coords_to_pixels(self, coords):
        return vec2d(coords[0] * 30 + 15, coords[1] * 30 + 15)

    def pixels_to_map_coords(self, coords):
        return vec2d(coords[0]//30, coords[1]//30)

    def draw(self, screen, focus):
        if type(self.static_content) == Wall:
            self.static_content.draw(screen, focus)

class Map():

    data = {}

    map_size = [0, 0]

    def __init__(self):
        map_file = open('assets/map.csv', 'r')
        map_line = map_file.readline()
        coords = [0, 0]
        while not map_line == '':
            cells = map_line.split(";")
            for cell in cells:
                    cell_info = cell.split("/")
                    if cell_info[1] == "0\n":
                        cell_info[1] = "0" 
                    key = '{0[0]},{0[1]}'.format(coords)
                    self.data[key] = Map_cell(vec2d(coords[0], coords[1]))
                    if not cell_info[0] == "0":
                        self.data[key].static_content = Wall(vec2d(coords[0], coords[1]), cell_info[0], cell_info[1])
                    coords[0] += 1
                    if coords[1] == 0:
                        self.map_size[0] += 30


            coords[1] += 1
            self.map_size[1] += 30
            coords[0] = 0
            map_line = map_file.readline()

    def define_wall(self, wall):
        pass

    def define_item(self, item):
        pass

    def draw(self, screen, focus):
        map_cell_focus = [focus[0]//30, focus[1]//30]
        for x in range(27):
            for y in range(20):
                coords = [int(map_cell_focus[0]) + x, int(map_cell_focus[1]) + y]
                key = '{0[0]},{0[1]}'.format(coords)
                print
                self.data[key].draw(screen, focus)



    
