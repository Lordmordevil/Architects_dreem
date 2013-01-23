from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *
from random import uniform

def generate_house(pos, buildings):
	def generate_room_walls(walls, base, start_pos):
		for x in range(base[0] + 1):
			for y in range(base[1] + 1):
				if x == 0 or x == base[0] or y == 0 or y == base[1]:
					walls.append(Wall(vec2d(start_pos[0] + x * 30, start_pos[1] + y * 30)))


	start_pos = vec2d(pos[0] - (pos[0] % 30), pos[1] - (pos[1] % 30))
	base = [int(uniform(10, 20)), int(uniform(10, 20))]
	room1 = [int(uniform(3, 10)), int(uniform(3, 10))]
	room2 = [int(uniform(3, 10)), int(uniform(3, 10))]
	room3 = [int(uniform(3, 15)), int(uniform(3, 10))]
	walls = []
	generate_room_walls(walls, base, start_pos)
	room1_start_pos = [start_pos[0] + (base[0] - room1[0]) * 30 ,start_pos[1] + (base[1] - room1[1]) * 30]
	generate_room_walls(walls, room1, room1_start_pos)
	room2_start_pos = [start_pos[0], start_pos[1] + (base[1] - room2[1]) * 30]
	generate_room_walls(walls, room2, room2_start_pos)
	room3_start_pos = [start_pos[0] + (base[0] - room3[0]) * 30, start_pos[1]]
	generate_room_walls(walls, room3, room3_start_pos)
	buildings.append(Building(walls))


class Wall():

	def __init__(self, pos):	
		self.pos = pos
		self.dir = 0

	def draw(self, screen, offset):
		pygame.draw.rect(screen, (90, 90, 90), (self.pos[0] - int(offset[0]), self.pos[1] - int(offset[1]), 30, 30))

class Building():

    def __init__(self, walls):
        self.walls = walls

    def draw(self, screen, offset):
        for wall in self.walls:
        	wall.draw(screen, offset)