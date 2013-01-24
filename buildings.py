from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from random import uniform

def load_map(buildings):
    map_file = open('assets/map.csv', 'r')

    map_line = map_file.readline()

    coords = [0, 0]

    while not map_line == '':
        cells = map_line.split(";")
        for cell in cells:
            cell_info = cell.split("/")
            if not cell_info[0] == "0":
                if cell_info[1] == "0/n":
                    cell_info[1] = "0"
                buildings.walls.append(Wall(vec2d(coords[0] * 30 + 15, coords[1] * 30 + 15), cell_info[0], cell_info[1]))
            coords[0] += 1


        coords[1] += 1
        coords[0] = 0
        map_line = map_file.readline()


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

class Buildings():

    def __init__(self):
        self.walls = []

    def draw(self, screen, focus):
        for wall in self.walls:
            wall.draw(screen, focus)
