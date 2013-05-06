import pygame

from vec2d import vec2d


class MapCell:
    pos = vec2d(0, 0)
    pasive_light_level = 0
    active_light_level = 0
    static_content = []
    entitys = []

    def __init__(self, pos):
        self.pos = pos

    def map_coords_to_pixels(self, coords):
        return vec2d(coords[0] * 30 + 15, coords[1] * 30 + 15)

    def pixels_to_map_coords(self, coords):
        return vec2d(coords[0] // 30, coords[1] // 30)

    def draw(self, screen, focus):
        screen_pos = vec2d(int(self.pos[0] * 30 - focus[0]), int(self.pos[1] * 30 - focus[1]))
        alpha = 25 * self.active_light_level

        pygame.draw.rect(screen, (alpha, alpha, alpha), (screen_pos[0], screen_pos[1], 30, 30))
        if type(self.static_content) == Wall and self.active_light_level > 0:
            self.static_content.draw(screen, focus, alpha)


class Wall:
    sprite_dict = {'1': "wall", '2': "door", '3': "window"}

    size = 25

    def __init__(self, pos, wall_type, direct):
        self.pos = pos
        self.dir = direct
        self.type = wall_type

        self.sprite = pygame.image.load("assets/obsticles/" + self.sprite_dict[wall_type] + ".png")
        if not direct == "0":
            self.sprite = pygame.transform.rotate(self.sprite, int(90 * (ord(direct) - 48)))

    def draw(self, screen, focus, alpha):
        screen_pos = vec2d(int(self.pos[0] * 30 + 15 - focus[0]), int(self.pos[1] * 30 + 15 - focus[1]))
        sprite_size = self.sprite.get_size()
        screen.blit(self.sprite,
                    (int(screen_pos[0] - sprite_size[0] // 2),
                     int(screen_pos[1] - sprite_size[1] // 2)),
                    special_flags=pygame.BLEND_MULT)


class Map:
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
                    self.data[key] = MapCell(vec2d(coords[0], coords[1]))
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

    def draw_light_map(self, player_pos):
        player_map_pos = [player_pos[0] // 30, player_pos[1] // 30]
        map_periferal_points = [[0, -9],
                                [1, -9],
                                [2, -9],
                                [3, -8],
                                [4, -8],
                                [5, -7],
                                [6, -7],
                                [7, -6],
                                [7, -5],
                                [8, -4],
                                [8, -3],
                                [9, -2],
                                [9, -1],
                                [9, 0]]

        for sign_x in range(2):
            for sign_y in range(2):
                for point in map_periferal_points:
                    ray = vec2d(point[0], point[1])
                    if sign_x == 1:
                        ray[0] *= -1
                    if sign_y == 1:
                        ray[1] *= -1
                    for length in range(36):
                        ray.length = length / 4 + 1
                        coords = [int(player_map_pos[0] + ray[0]), int(player_map_pos[1] + ray[1])]
                        key = '{0[0]},{0[1]}'.format(coords)
                        if self.data[key].active_light_level == self.data[key].pasive_light_level or self.data[key].active_light_level == 0:
                            self.data[key].active_light_level = self.data[key].pasive_light_level + 8 - int(length / 4)
                            if self.data[key].active_light_level > 7:
                                self.data[key].active_light_level = 7
                        if type(self.data[key].static_content) == Wall and not self.data[key].static_content.type == "3":
                            break

    def draw(self, screen, focus, player_pos):
        map_cell_focus = [focus[0] // 30, focus[1] // 30]
        self.draw_light_map(player_pos)
        for x in range(27):
            for y in range(20):
                coords = [int(map_cell_focus[0]) + x, int(map_cell_focus[1]) + y]
                key = '{0[0]},{0[1]}'.format(coords)
                self.data[key].draw(screen, focus)

    def reset(self):
        for cell in self.data:
            if self.data[cell].active_light_level != self.data[cell].pasive_light_level:
                self.data[cell].active_light_level = self.data[cell].pasive_light_level
