#External inputs, boundary restrictions

import mg_function
import pygame
from numpy import zeros, floor, ceil
from enum import Enum, IntEnum


# Static
fps = 800
display_surf_width_pixel = 1280
display_surf_height_pixel = 720

grid_size_pixel = 64
wall_thickness_pixel = 2
row_num = 8
column_num = 8
start_grid_num = 1
growth_ratio = 0.2
mask = zeros((row_num, column_num))

sampling_size = 1000
output_file_path = 'V2020_output.txt'




# Dynamic
d_fps = {
    'LOW'       : 4,
    'NORMAL'    : 60,
    'HIGH'      : 800,
}

d_display_surf_size_pixel = {
    'SVGA'      : [800, 600],
    'XGA'       : [1024, 768],
    'HD'        : [1280, 720],
    'HDTV'      : [1920, 1080],
}

d_grid_size_pixel = {
    'SMALL'     : 16,
    'NORMAL'    : 32,
    'LARGE'     : 64,
}

d_wall_thickness_pixel = {
    'THIN'      : 1,
    'NORMAL'    : 2,
    'THICK'     : 4,
}

d_map_size = {
    'SQ_SMALL'      : [8, 8],
    'SQ_NORMAL'     : [16, 16],
    'SQ_LARGE'      : [32, 32],
    'RECT_SMALL'    : [8, 16],
    'RECT_NORMAL'   : [16, 32],
    'RECT_LARGE'    : [32, 64],
}

d_map_shape = {
    'SQ_SMALL'      : (d_map_size['SQ_SMALL'], d_wall_thickness_pixel['THICK'], d_grid_size_pixel['LARGE']),
    'SQ_NORMAL'     : (d_map_size['SQ_NORMAL'], d_wall_thickness_pixel['NORMAL'], d_grid_size_pixel['NORMAL']),
    'SQ_LARGE'      : (d_map_size['SQ_LARGE'], d_wall_thickness_pixel['NORMAL'], d_grid_size_pixel['SMALL']),
    'RECT_SMALL'    : (d_map_size['RECT_SMALL'], d_wall_thickness_pixel['THICK'], d_grid_size_pixel['LARGE']),
    'RECT_NORMAL'   : (d_map_size['RECT_NORMAL'], d_wall_thickness_pixel['NORMAL'], d_grid_size_pixel['NORMAL']),
    'RECT_LARGE'    : (d_map_size['RECT_LARGE'], d_wall_thickness_pixel['NORMAL'], d_grid_size_pixel['SMALL']),
}

mask_empty = zeros((32, 64))

mask_cut_a_corner = zeros((32, 64))
for i in range(16, 32):
    for j in range(16):
        mask_cut_a_corner[i][j] = 1

mask_cut_in_mid = zeros((32, 64))
for i in range(8, 24):
    for j in range(24, 48):
        mask_cut_in_mid[i][j] = 1

mask_more = zeros((32, 64))
for i in range(16, 32):
    for j in range(16):
        mask_more[i][j] = 1
for i in range(8, 24):
    for j in range(24, 48):
        mask_more[i][j] = 1

d_mask = {
    'EMPTY'         : mask_empty,
    'CUT_CORNER'    : mask_cut_a_corner,
    'CUT_MID'       : mask_cut_in_mid,
    'CUT_MORE'      : mask_more,
}

d_start_grid_mode = {
#    'FIXED'     : 1,
    'RANDOM'    : 0,
}

d_start_grid_num = {
    'SINGLE'    : 1,
    'FEW'       : 4,
    'SOME'      : 8,
    'MANY'      : 16,
#    'DANGEROUS' : 32,
}

d_entrance_exit_mode = {
    'FIXED'     : 1,
    'RANDOM'    : 0,
    'DERIVED'   : -1,
}

d_growth_ratio = {
    'LOW'       : 0.05,
    'NORMAL'    : 0.2,
    'HIGH'      : 0.4,
    'ONE'       : 1,
}

d_wall_only_mode = {
    'ON'    : True,
    'OFF'   : False,
}

d_display_grid_color = {
    'NO'            : 0,
    'TO_START_GRID': 1,
    'TO_ROUTE'      : 2,
    'STATUS'        : 3,
}

d_display_grid_distance = {
    'ON'    : True,
    'OFF'   : False,
}

d_display_generation_process = {
    'ON'    : True,
    'OFF'   : False,
}

d_display_route = {
    'ON'    : True,
    'OFF'   : False,
}


d_button_status = {
    'UP'                : 0,
    'MOUSE_OVER_UP'    : 1,
    'PRESSED'           : 2,
    'MOUSE_OVER_DOWN'  : 3,
    'DOWN'              : 4,
}

d_button_color = {
    'RED_2'     : (255, 0, 0),
    'RED_1'     : (192, 0, 0),
    'RED_3'     : (128, 0, 0),
    'BLUE'      : (0, 0, 255),
    'NAVY_BLUE' : (0, 0, 192),
    'BLACK'     : (0, 0, 0),
    'GREY_3'    : (32, 32, 32),
    'GREY_2'    : (64, 64, 64),
    'GREY_1'    : (128, 128, 128),
    'GREY_4'    : (192, 192, 192),
    'WHITE'     : (255, 255, 255),
}


# Management button list
# key : ((pos_x, pos_y, width, height), type, default_value)
# (0 : 1280) * (0 : 640) for displaying map
# (1280 : 1880) * (40 : 640) for map generation configs
# (1280 : 1880) * (640 : 1080) for map displaying configs
# (1280 : 1480) for config keys, (1480 : 1880) for buttons
# (0 : 1280) * (640 : 800) for map description
# (0 : 1280) * (800 : 1080) for map statistics
# (1880 : 1920) * (0 : 40) exit button
d_button_group_map = {
    'Map Shape': ((1200, 40, 680, 80), d_map_shape, d_map_shape['SQ_NORMAL']),
    'Start Grid Mode': ((1200, 140, 680, 80), d_start_grid_mode, d_start_grid_mode['RANDOM']),
    'Start Grid Number': ((1200, 240, 680, 80), d_start_grid_num, d_start_grid_num['FEW']),
    'Entrance and Exit Mode': ((1200, 340, 680, 80), d_entrance_exit_mode, d_entrance_exit_mode['RANDOM']),
    'Growth Ratio': ((1200, 440, 680, 80), d_growth_ratio, d_growth_ratio['NORMAL']),
}

generate_button_pos = (1520, 600, 120, 60)

d_button_group_display = {
    'Colored Grids': ((1200, 720, 680, 60), d_display_grid_color, d_display_grid_color['TO_START_GRID']),
    'Numbered Grids': ((1200, 800, 680, 60), d_display_grid_distance, d_display_grid_distance['ON']),
    'Display Generation': ((1200, 880, 680, 60), d_display_generation_process, d_display_generation_process['ON']),
    'Display Route': ((1200, 960, 680, 60), d_display_route, d_display_route['ON']),
}

exit_button_pos = (1880, 0, 40, 40)

map_description_pos = (0, 640, 1280, 160)

d_map_statistics = {
    'Route Length': (160, 840, 560, 100),
    'Number of Turns': (720, 840, 560, 100),
    'Average Distance to Route': (160, 940, 560, 100),
    'Maximum Distance to Route': (720, 940, 560, 100),
}


class config_list_index(IntEnum):
    MAP_SHAPE                   = 0
    START_GRID_MODE             = 1
    START_GRID_NUM              = 2
    ENTRANCE_EXIT_MODE          = 3
    GROWTH_RATIO                = 4
    DISPLAY_GRID_COLOR          = 5
    DISPLAY_GRID_DISTANCE       = 6
    DISPLAY_GENERATION_PROCESS  = 7
    DISPLAY_ROUTE               = 8

class button_ret(Enum):
    NOTHING                 = 0
    UPDATE_CONFIG_MAP       = 1
    UPDATE_CONFIG_DISPLAY   = 2
    GENERATE_MAP            = 3
    EXIT                    = 4


# In table form
class boundary_condition_struct:
    def __init__(self, description, in_fps, in_surf_width, in_surf_height,
                 in_grid_size, in_wall_thickness, in_row, in_column, in_mask,
                 in_start_num, in_ratio):
        self.description = description
        self.fps = in_fps
        self.display_surf_width_pixel = in_surf_width
        self.display_surf_height_pixel = in_surf_height

        self.grid_size_pixel = in_grid_size
        self.wall_thickness = in_wall_thickness
        self.row_num = in_row
        self.column_num = in_column
        self.start_grid_num = in_start_num
        self.growth_ratio = in_ratio
        self.mask = in_mask

        return


# For application
class config_application:
    def __init__(self):
        self.display_surf_width_pixel = d_display_surf_size_pixel['HDTV'][0]
        self.display_surf_height_pixel = d_display_surf_size_pixel['HDTV'][1]
        self.fps = d_fps['NORMAL']

        return


# Not used
class config_map:
    def __init__(self):
        # Size
        self.row_num = d_map_size['SQ_NORMAL'][0]
        self.column_num = d_map_size['SQ_NORMAL'][1]

        # Hidden
        self.mask = d_mask['EMPTY']
        self.start_grid_list = None
        # Currently, used top-left corner and bottom-right corner for 'FIX' mode
        self.entrance_exit = None

        # Generation
        self.start_grid_mode = d_start_grid_mode['RANDOM']
        self.start_grid_num = d_start_grid_num['FEW']
        self.entrance_exit_mode = d_entrance_exit_mode['FIXED']
        self.growth_ratio = d_growth_ratio['NORMAL']

        return


# Not used
class config_display:
    def __init__(self):
        self.display_wall_only = d_wall_only_mode['OFF']
        self.display_grid_color = d_display_grid_color['TO_START_GRID']
        self.display_grid_distance = d_display_grid_distance['ON']
        self.display_generation_process = d_display_generation_process['ON']
        self.display_route = d_display_route['ON']

        return


class config_management:
    def __init__(self):
        self.display_surf = None
        self.config_list = list()
        self.button_group_list_map = list()
        self.button_group_list_display = list()
        self.button_list = list()

        return


    def init_button_group_list(self, display_surf):
        self.display_surf = display_surf

        index = 0
        for button_group in d_button_group_map:
            self.config_list.append(d_button_group_map[button_group][2])
            self.button_group_list_map.append(mg_button_group(self, display_surf, button_group,
                                                              d_button_group_map[button_group], index))
            index += 1

        for button_group in d_button_group_display:
            self.config_list.append(d_button_group_display[button_group][2])
            self.button_group_list_display.append(mg_button_group(self, display_surf, button_group,
                                                                  d_button_group_display[button_group], index))
            index += 1

        self.button_list.append(mg_button(display_surf, 'Generate', generate_button_pos, 0, d_button_status['UP']))
        self.button_list.append(mg_button(display_surf, 'X', exit_button_pos, 0, d_button_status['UP']))

        return


    def on_mouse_over(self, mouse_pos):
        ret = button_ret.NOTHING

        for button_group in self.button_group_list_map:
            if button_group.on_mouse_over(mouse_pos):
                ret = button_ret.UPDATE_CONFIG_MAP

        for button_group in self.button_group_list_display:
            if button_group.on_mouse_over(mouse_pos):
                ret = button_ret.UPDATE_CONFIG_DISPLAY

        if self.button_list[0].on_mouse_over(mouse_pos):
            ret = button_ret.GENERATE_MAP

        if self.button_list[1].on_mouse_over(mouse_pos):
            ret = button_ret.EXIT

        return ret


    def on_pressed(self, mouse_pos):
        ret = button_ret.NOTHING

        for button_group in self.button_group_list_map:
            if button_group.on_pressed(mouse_pos):
                ret = button_ret.UPDATE_CONFIG_MAP

        for button_group in self.button_group_list_display:
            if button_group.on_pressed(mouse_pos):
                ret = button_ret.UPDATE_CONFIG_DISPLAY

        if self.button_list[0].on_pressed(mouse_pos):
            ret = button_ret.GENERATE_MAP

        if self.button_list[1].on_pressed(mouse_pos):
            ret = button_ret.EXIT

        return ret


    def on_click(self, mouse_pos):
        ret = button_ret.NOTHING

        for button_group in self.button_group_list_map:
            if button_group.on_click(mouse_pos):
                ret = button_ret.UPDATE_CONFIG_MAP

        for button_group in self.button_group_list_display:
            if button_group.on_click(mouse_pos):
                ret = button_ret.UPDATE_CONFIG_DISPLAY

        if self.button_list[0].on_click(mouse_pos):
            ret = button_ret.GENERATE_MAP

        if self.button_list[1].on_click(mouse_pos):
            ret = button_ret.EXIT

        return ret


    def display_buttons(self):
        for button_group in self.button_group_list_map:
            button_group.display()
        for button_group in self.button_group_list_display:
            button_group.display()
        for button in self.button_list:
            button.display()

        return


    def display_update(self):
        for button_group in self.button_group_list_map:
            button_group.display_update()
        for button_group in self.button_group_list_display:
            button_group.display_update()
        for button in self.button_list:
            button.display_update()

        return


    def display_map_description(self):
        text = str(self.config_list[config_list_index.MAP_SHAPE][0][0]) + '*' \
               + str(self.config_list[config_list_index.MAP_SHAPE][0][1]) + '  ' \
               + str(mg_function.getDictionaryKeyWithValue(d_start_grid_num, self.config_list[config_list_index.START_GRID_NUM])) + '-' \
               + str(mg_function.getDictionaryKeyWithValue(d_start_grid_mode, self.config_list[config_list_index.START_GRID_MODE])) + '-START-GRID  ' \
               + str(mg_function.getDictionaryKeyWithValue(d_entrance_exit_mode, self.config_list[config_list_index.ENTRANCE_EXIT_MODE])) + '-ENTRANCE & EXIT  ' \
               + str(mg_function.getDictionaryKeyWithValue(d_growth_ratio, self.config_list[config_list_index.GROWTH_RATIO])) + '-GROWTH RATIO'
        pygame.draw.rect(self.display_surf, d_button_color['BLACK'], map_description_pos)
        text_surf, text_rect = mg_function.textDisplay(text, "comicsansms", 24, d_button_color['NAVY_BLUE'],
                                                       map_description_pos[0] + map_description_pos[2] / 2,
                                                       map_description_pos[1] + map_description_pos[3] / 2)
        self.display_surf.blit(text_surf, text_rect)

        return


    def display_map_statistics(self, map_statistics):
        i = 0
        for statistic in d_map_statistics:
            pos_set = d_map_statistics[statistic]
            pygame.draw.rect(self.display_surf, d_button_color['BLACK'], pos_set)
            pos_set = d_map_statistics[statistic]
            text_surf, text_rect \
                = mg_function.textDisplayTopLeftAligned(statistic, "comicsansms", 24,
                                                        d_button_color['NAVY_BLUE'],
                                                        pos_set[0], pos_set[1])
            self.display_surf.blit(text_surf, text_rect)
            text_surf, text_rect \
                = mg_function.textDisplayTopLeftAligned(str(map_statistics[i]), "comicsansms", 24,
                                                        d_button_color['NAVY_BLUE'],
                                                        pos_set[0] + 0.6 * pos_set[2], pos_set[1])
            self.display_surf.blit(text_surf, text_rect)

            i += 1

        return


# Constants for buttons
default_button_press_depth = 4
up_color = d_button_color['GREY_1']
mouse_over_up_color = d_button_color['GREY_4']
on_click_color = d_button_color['RED_3']
mouse_over_down_color = d_button_color['RED_2']
down_color = d_button_color['RED_1']
text_color = d_button_color['NAVY_BLUE']

MAX_OPTION_NUM = 6


class mg_button:
    def __init__(self, display_surf, text, pos_set,
                 index, button_status):
        self.display_surf = display_surf
        self.text = text
        self.pos_x = pos_set[0]
        self.pos_y = pos_set[1]
        self.width = pos_set[2]
        self.height = pos_set[3]

        self.index = index
        self.button_status = button_status
        self.button_status_display = button_status
        self.status_changed = False

        self.up_color = up_color
        self.mouse_over_up_color = mouse_over_up_color
        self.on_click_color = on_click_color
        self.mouse_over_down_color = mouse_over_down_color
        self.down_color = down_color
        self.text_color = text_color

        # width and height should be bigger than 2 * press_depth
        self.press_depth = default_button_press_depth
        if self.width < 2 * self.press_depth:
            self.press_depth = floor(self.width / 2)
        if self.height < 2 * self.press_depth:
            self.press_depth = floor(self.height / 2)

        return


    def is_pointed(self, mouse_pos):
        if self.pos_x < mouse_pos[0] < self.pos_x + self.width \
                and self.pos_y < mouse_pos[1] < self.pos_y + self.height:
            return True
        else:
            return False


    def on_mouse_over(self, mouse_pos):
        ret = False

        if self.is_pointed(mouse_pos):
            ret = True
            if self.button_status_display != d_button_status['MOUSE_OVER_UP'] \
                    and self.button_status_display != d_button_status['MOUSE_OVER_DOWN']:
                self.status_changed = True
                if self.button_status_display == d_button_status['UP']:
                    self.button_status_display = d_button_status['MOUSE_OVER_UP']
                else:
                    self.button_status_display = d_button_status['MOUSE_OVER_DOWN']
        else:
            if self.button_status_display != self.button_status:
                self.status_changed = True
                self.button_status_display = self.button_status

        return ret


    def on_pressed(self, mouse_pos):
        ret = False

        if self.is_pointed(mouse_pos):
            ret = True
            if self.button_status_display != d_button_status['PRESSED']:
                self.status_changed = True
                self.button_status_display = d_button_status['PRESSED']
        else:
            if self.button_status_display != self.button_status:
                self.status_changed = True
                self.button_status_display = self.button_status

        return ret


    def on_click(self, mouse_pos):
        ret = False

        if self.is_pointed(mouse_pos):
            ret = True
            if self.button_status_display != d_button_status['MOUSE_OVER_UP']:
                self.status_changed = True
                self.button_status_display = d_button_status['MOUSE_OVER_UP']
        else:
            if self.button_status_display != self.button_status:
                self.status_changed = True
                self.button_status_display = self.button_status

        return ret


    def set_status(self, button_status):
        if self.button_status != button_status:
            self.button_status = button_status
            self.status_changed = True

        return


    def display(self):
        if self.button_status_display == d_button_status['UP']:
            pygame.draw.rect(self.display_surf, d_button_color['BLACK'],
                             (self.pos_x, self.pos_y, self.width, self.height))
            pygame.draw.rect(self.display_surf, d_button_color['GREY_2'],
                             (self.pos_x + self.press_depth, self.pos_y + self.press_depth,
                              self.width - self.press_depth, self.height - self.press_depth))
            pygame.draw.rect(self.display_surf, self.up_color,
                             (self.pos_x, self.pos_y,
                              self.width - self.press_depth, self.height - self.press_depth))
            text_surf, text_rect \
                = mg_function.textDisplay(self.text, "comicsansms",
                                          int(ceil((self.height - self.press_depth) / 4)), self.text_color,
                                          self.pos_x + (self.width - self.press_depth) / 2,
                                          self.pos_y + (self.height - self.press_depth) / 2)
            self.display_surf.blit(text_surf, text_rect)
        elif self.button_status_display == d_button_status['MOUSE_OVER_UP']:
            pygame.draw.rect(self.display_surf, d_button_color['BLACK'],
                             (self.pos_x, self.pos_y, self.width, self.height))
            pygame.draw.rect(self.display_surf, d_button_color['GREY_2'],
                             (self.pos_x + self.press_depth, self.pos_y + self.press_depth,
                              self.width - self.press_depth, self.height - self.press_depth))
            pygame.draw.rect(self.display_surf, self.mouse_over_up_color,
                             (self.pos_x, self.pos_y,
                              self.width - self.press_depth, self.height - self.press_depth))
            text_surf, text_rect \
                = mg_function.textDisplay(self.text, "comicsansms",
                                          int(ceil((self.height - self.press_depth) / 4)), self.text_color,
                                          self.pos_x + (self.width - self.press_depth) / 2,
                                          self.pos_y + (self.height - self.press_depth) / 2)
            self.display_surf.blit(text_surf, text_rect)
        elif self.button_status_display == d_button_status['PRESSED']:
            pygame.draw.rect(self.display_surf, d_button_color['BLACK'],
                             (self.pos_x, self.pos_y, self.width, self.height))
            pygame.draw.rect(self.display_surf, d_button_color['GREY_2'],
                             (self.pos_x + self.press_depth, self.pos_y + self.press_depth,
                              self.width - self.press_depth, self.height - self.press_depth))
            pygame.draw.rect(self.display_surf, self.on_click_color,
                             (self.pos_x + 2 * self.press_depth, self.pos_y + 2 * self.press_depth,
                              self.width - 2 * self.press_depth, self.height - 2 * self.press_depth))
            text_surf, text_rect \
                = mg_function.textDisplay(self.text, "comicsansms",
                                          int(ceil((self.height - self.press_depth) / 4)), self.text_color,
                                          self.pos_x + self.width / 2 + self.press_depth,
                                          self.pos_y + self.height / 2 + self.press_depth)
            self.display_surf.blit(text_surf, text_rect)
        elif self.button_status_display == d_button_status['MOUSE_OVER_DOWN']:
            pygame.draw.rect(self.display_surf, d_button_color['BLACK'],
                             (self.pos_x, self.pos_y, self.width, self.height))
            pygame.draw.rect(self.display_surf, self.mouse_over_down_color,
                             (self.pos_x + self.press_depth, self.pos_y + self.press_depth,
                              self.width - self.press_depth, self.height - self.press_depth))
            text_surf, text_rect \
                = mg_function.textDisplay(self.text, "comicsansms",
                                          int(ceil((self.height - self.press_depth) / 4)), self.text_color,
                                          self.pos_x + (self.width + self.press_depth) / 2,
                                          self.pos_y + (self.height + self.press_depth) / 2)
            self.display_surf.blit(text_surf, text_rect)
        elif self.button_status_display == d_button_status['DOWN']:
            pygame.draw.rect(self.display_surf, d_button_color['BLACK'],
                             (self.pos_x, self.pos_y, self.width, self.height))
            pygame.draw.rect(self.display_surf, self.down_color,
                             (self.pos_x + self.press_depth, self.pos_y + self.press_depth,
                              self.width - self.press_depth, self.height - self.press_depth))
            text_surf, text_rect \
                = mg_function.textDisplay(self.text, "comicsansms",
                                          int(ceil((self.height - self.press_depth) / 4)), self.text_color,
                                          self.pos_x + (self.width + self.press_depth) / 2,
                                          self.pos_y + (self.height + self.press_depth) / 2)
            self.display_surf.blit(text_surf, text_rect)

        return


    def display_update(self):
        if self.status_changed is False:
            return

        self.display()
        self.status_changed = False

        return


class mg_button_group:
    def __init__(self, config_management, display_surf, text, button_group_info, index):
        self.config_management = config_management
        self.display_surf = display_surf
        self.text = text
        self.text_color = text_color
        self.index = index

        pos_set = button_group_info[0]
        self.option_set = button_group_info[1]
        self.pos_x = pos_set[0]
        self.pos_y = pos_set[1]
        self.width = pos_set[2]
        self.height = pos_set[3]
        self.button_list = list()

        pos_x = self.pos_x + 0.4 * self.width
        pos_y = self.pos_y + 0.6 * self.height
        width = 0.6 * self.width / MAX_OPTION_NUM
        height = 0.4 * self.height
        index = 0

        for button in self.option_set:
            if button_group_info[2] == self.option_set[button]:
                self.button_list.append(mg_button(display_surf, button,
                                                  (pos_x, pos_y, width - 4 * default_button_press_depth, height),
                                                  index, d_button_status['DOWN']))
            else:
                self.button_list.append(mg_button(display_surf, button,
                                                  (pos_x, pos_y, width - 4 * default_button_press_depth, height),
                                                  index, d_button_status['UP']))
            pos_x += width
            index += 1

        return


    def on_mouse_over(self, mouse_pos):
        ret = False

        for button in self.button_list:
            if button.is_pointed(mouse_pos):
                ret = True
                if button.button_status_display != d_button_status['MOUSE_OVER_UP'] \
                        and button.button_status_display != d_button_status['MOUSE_OVER_DOWN']:
                    button.status_changed = True
                    if button.button_status_display == d_button_status['UP']:
                        button.button_status_display = d_button_status['MOUSE_OVER_UP']
                    else:
                        button.button_status_display = d_button_status['MOUSE_OVER_DOWN']
            else:
                if button.button_status_display != button.button_status:
                    button.status_changed = True
                    button.button_status_display = button.button_status

        return ret


    def on_pressed(self, mouse_pos):
        ret = False

        for button in self.button_list:
            if button.is_pointed(mouse_pos):
                ret = True
                if button.button_status_display != d_button_status['PRESSED']:
                    button.status_changed = True
                    button.button_status_display = d_button_status['PRESSED']
            else:
                if button.button_status_display != button.button_status:
                    button.status_changed = True
                    button.button_status_display = button.button_status

        return ret


    def on_click(self, mouse_pos):
        ret = False

        for button in self.button_list:
            if button.is_pointed(mouse_pos):
                ret = True
                if button.button_status_display != d_button_status['MOUSE_OVER_DOWN']:
                    button.status_changed = True
                    button.button_status_display = d_button_status['MOUSE_OVER_DOWN']
                if button.button_status != d_button_status['DOWN']:
                    button.button_status = d_button_status['DOWN']
                    self.config_management.config_list[self.index] = self.option_set[button.text]
            else:
                if button.button_status_display != button.button_status:
                    button.status_changed = True
                    button.button_status_display = button.button_status

        if ret is True:
            for button in self.button_list:
                if self.config_management.config_list[self.index] != self.option_set[button.text] \
                        and button.button_status == d_button_status['DOWN']:
                    button.status_changed = True
                    button.button_status = d_button_status['UP']
                    button.button_status_display = button.button_status

        return ret


    def display(self):
        text_surf, text_rect \
            = mg_function.textDisplayTopLeftAligned(self.text, "comicsansms",
                                                    int(ceil(self.height / 4)), self.text_color,
                                                    self.pos_x + 0.2 * self.width, self.pos_y + 0.2 * self.height)
        self.display_surf.blit(text_surf, text_rect)
        for button in self.button_list:
            button.display()

        return


    def display_update(self):
        for button in self.button_list:
            button.display_update()

        return


    def set_status_all_buttons(self, button_status):
        for button in self.button_list:
            button.set_status(button_status)

        return


    def set_status_one_button(self, button_status, index):
        if index < self.button_list.__len__():
            self.button_list[index].set_status(button_status)

        return

