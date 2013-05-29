from vec2d import vec2d
from map import Wall
from settings import CELL_SIZE

def draw_to_screen(self, screen, image, pos):
    pass

def collider(obj, world_map, size, obj_type):
    object_pos = vec2d(obj.pos[0] // CELL_SIZE, obj.pos[1] // CELL_SIZE)
    for x in range(3):
        for y in range(3):
            coords = [int(object_pos[0]) - 1 + x, int(object_pos[1]) - 1 + y]
            key = '{0[0]},{0[1]}'.format(coords)
            cell = world_map.data[key]
            for friend in cell.entitys:
                if not friend == obj:
                    dist = obj.pos.get_distance(friend.pos)
                    if dist < size:
                        overlap = size - dist
                        ndir = friend.pos - obj.pos
                        ndir.length = overlap
                        ndir.length = ndir.length / 2
                        friend.pos = friend.pos + ndir
                        obj.pos = obj.pos - ndir
                        if obj_type == "player":
                            if obj.health < 1:
                                obj.health = 0
                            else:
                                obj.health -= 1
                                if friend.health + 1 < friend.max_health:
                                    friend.health += 1


def wall_collider(obj, world_map, size):
    object_pos = vec2d(obj.pos[0] // CELL_SIZE, obj.pos[1] // CELL_SIZE)
    passable = ["2"]
    for x in range(3):
        for y in range(3):
            coords = [int(object_pos[0]) - 1 + x, int(object_pos[1]) - 1 + y]
            key = '{0[0]},{0[1]}'.format(coords)
            cell = world_map.data[key]
            if type(cell.static_content) == Wall and not cell.static_content.type in passable:
                dist = obj.pos.get_distance(cell.map_coords_to_pixels(cell.static_content.pos))
                if dist < size + 10:
                    overlap = int(size + 10) - dist
                    ndir = cell.map_coords_to_pixels(cell.static_content.pos) - obj.pos
                    ndir.length = overlap
                    obj.pos = obj.pos - ndir


def update_focus(alt_player_pos, focus, world_map):
    if alt_player_pos[0] > 500 and focus[0] < world_map.map_size[0] - 830:
        focus[0] += alt_player_pos[0] - 500
    if alt_player_pos[1] > 350 and focus[1] < world_map.map_size[1] - 630:
        focus[1] += alt_player_pos[1] - 350
    if alt_player_pos[0] < 300 and focus[0] > CELL_SIZE:
        focus[0] -= 300 - alt_player_pos[0]
    if alt_player_pos[1] < 250 and focus[1] > CELL_SIZE:
        focus[1] -= 250 - alt_player_pos[1]
