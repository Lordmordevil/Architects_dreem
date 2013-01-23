from pygamehelper import *
from pygame import *
from pygame.locals import *
from vec2d import *

def debug_static_map(screen, focus, screen_width, screen_height):
        def draw_colmn(x_pos, height, screen):
            for lines in range((height // 10)):
                pygame.draw.line(screen, (220, 220, 220), (x_pos, lines * 10), (x_pos, (lines * 10) + 5)) 

        def draw_row(y_pos, height, screen):
            for lines in range((height // 10)):
                pygame.draw.line(screen, (220, 220, 220), (lines * 10, y_pos), ((lines * 10) + 5, y_pos))

        box_size = 30
        offset = vec2d(0, 0)
        offset[0] = focus[0] % box_size
        offset[1] = focus[1] % box_size
        width_line_count = screen_width//box_size
        height_line_count = screen_height//box_size
        for colmn in range(width_line_count + 1):
            draw_colmn(colmn * box_size - offset[0], screen_height, screen)
        for row in range(height_line_count + 1):
            draw_row(row * box_size - offset[1], screen_width, screen)