# Definitions of constants

# Imports
import mg_boundary, mg_function
import pygame
from numpy import sum, ceil, sqrt, zeros, ones
from enum import Enum


# Colors RGB
color = {
    'RED'       : (255, 0, 0),
    'BLUE'      : (0, 0, 255),
    'BLACK'     : (0, 0, 0),
    'GREY_3'    : (64, 64, 64),
    'GREY_2'    : (128, 128, 128),
    'GREY_1'    : (192, 192, 192),
    'WHITE'     : (255, 255, 255),
}


# Status
class status(Enum):
    NOTHING     = -1    #the border of the map
    NEWBORN     = 0     #grid barely initialized
    GROWING     = 1     #new grid adjacent to the closure of mature grids
    MATURE      = 2     #the edge of the closure of mature grids
    GRAVEN      = 3     #grid fully used



# Grid of the Map
# Basic
class basic_grid_2d_square:
    def __init__(self, x, y, up, left):
        # Pos for position
        self.pos_x = x
        self.pos_y = y

        # Status
        self.status = status.NOTHING
        self.on_route = False
        self.distance = None

        # nb for neighbor
        self.nb_up = up
        self.nb_down = None
        if up is not None:
            up.nb_down = self
        self.nb_left = left
        self.nb_right = None
        if left is not None:
            left.nb_right = self

        # Connections
        self.conn_to_up = False
        self.conn_to_left = False

        return


    def display_floor(self, display_surf, origin_pos_x, origin_pos_y, color_gradient, grid_size):
        # Set grid color
        if self.status == status.NEWBORN:
            display_color = color['GREY_3']
        elif self.status == status.GROWING:
            display_color = color['GREY_2']
        elif self.status == status.MATURE:
            display_color = color['GREY_1']
        elif self.status == status.GRAVEN:
            display_color = color['WHITE']
        else:
            display_color = color['BLACK']

        # Show distance by color
        if self.distance is not None:
            origin_color = list(color['RED'])
            color_shift = [-2 * color_gradient * self.distance,
                           color_gradient * self.distance, color_gradient * self.distance]
            curr_color = sum([origin_color, color_shift], axis=0)
            display_color = tuple(mg_function.colorValidation(curr_color))

        # Allocate top left point
        grid_origin_pos_x = origin_pos_x + grid_size * self.pos_x
        grid_origin_pos_y = origin_pos_y + grid_size * self.pos_y

        # Draw floor
        display_pos = (grid_origin_pos_y, grid_origin_pos_x,
                       grid_size, grid_size)
        pygame.draw.rect(display_surf, display_color, display_pos)

        return


    def display_distance(self, display_surf, origin_pos_x, origin_pos_y, grid_size):
        # Allocate top left point
        grid_origin_pos_x = origin_pos_x + grid_size * self.pos_x
        grid_origin_pos_y = origin_pos_y + grid_size * self.pos_y

        # Show distance by text
        text_color = color['BLUE']
        if self.on_route is True:
            text_color = color['WHITE']
        if self.distance is not None:
            text_surf, text_rect \
                = mg_function.textDisplay(str(int(self.distance)), "comicsansms",
                                          int(ceil(grid_size / 2)), text_color,
                                          grid_origin_pos_y + grid_size / 2, grid_origin_pos_x + grid_size / 2)
            display_surf.blit(text_surf, text_rect)

        return


    def display_wall(self, display_surf, origin_pos_x, origin_pos_y, grid_size):
        # Allocate top left point
        grid_origin_pos_x = origin_pos_x + grid_size * self.pos_x
        grid_origin_pos_y = origin_pos_y + grid_size * self.pos_y

        # Draw walls
        wall_color = color['BLUE']
        if self.conn_to_up is False:
            pygame.draw.line(display_surf, wall_color, (grid_origin_pos_y, grid_origin_pos_x),
                             (grid_origin_pos_y + grid_size, grid_origin_pos_x),
                             mg_boundary.wall_thickness_pixel)
        if self.conn_to_left is False:
            pygame.draw.line(display_surf, wall_color, (grid_origin_pos_y, grid_origin_pos_x),
                             (grid_origin_pos_y, grid_origin_pos_x + grid_size),
                             mg_boundary.wall_thickness_pixel)

        return


# Improved
class improved_grid_2d_square(basic_grid_2d_square):
    def __init__(self, x, y, up, left):
        # Inherit
        basic_grid_2d_square.__init__(self, x, y, up, left)

        # Status
        self.status_changed = True
        self.connected_area = 0

        # Walls
        self.wall_up = None
        self.wall_down = None
        self.wall_left = None
        self.wall_right = None

        # Distance
        self.distance_to_route = -1

        return


    def display_floor_update(self, display_surf, origin_pos_x, origin_pos_y, color_gradient, grid_size,
                             display_grid_color):
        if self.status_changed is False:
            return

        display_color = color['BLACK']

        # Set grid color by status
        if display_grid_color == mg_boundary.d_display_grid_color['STATUS']:
            if self.status == status.NEWBORN:
                display_color = color['GREY_3']
            elif self.status == status.GROWING:
                display_color = color['GREY_2']
            elif self.status == status.MATURE:
                display_color = color['GREY_1']
            elif self.status == status.GRAVEN:
                display_color = color['WHITE']

        # Show distance to start grid by color
        if display_grid_color == mg_boundary.d_display_grid_color['TO_START_GRID'] \
                and self.distance is not None:
            origin_color = list(color['RED'])
            color_shift = [-2 * color_gradient * self.distance,
                           color_gradient * self.distance, color_gradient * self.distance]
            curr_color = sum([origin_color, color_shift], axis=0)
            display_color = tuple(mg_function.colorValidation(curr_color))

        # Show distance to route by color
        if display_grid_color == mg_boundary.d_display_grid_color['TO_ROUTE'] \
                and self.distance_to_route != -1:
            origin_color = list(color['RED'])
            color_shift = [-1 * color_gradient * self.distance_to_route,
                           0.5 * color_gradient * self.distance_to_route, 0.5 * color_gradient * self.distance_to_route]
            curr_color = sum([origin_color, color_shift], axis=0)
            display_color = tuple(mg_function.colorValidation(curr_color))

        # Allocate top left point
        grid_origin_pos_x = origin_pos_x + grid_size * self.pos_x
        grid_origin_pos_y = origin_pos_y + grid_size * self.pos_y

        # Draw floor
        display_pos = (grid_origin_pos_y, grid_origin_pos_x, grid_size, grid_size)
        pygame.draw.rect(display_surf, display_color, display_pos)

        return


    def display_distance_update(self, display_surf, origin_pos_x, origin_pos_y, grid_size,
                                display_grid_color, display_route):
        if self.status_changed is False:
            return

        # Allocate top left point
        grid_origin_pos_x = origin_pos_x + grid_size * self.pos_x
        grid_origin_pos_y = origin_pos_y + grid_size * self.pos_y

        # Show distance by text
        text_color = color['BLUE']
        if display_route is True and self.on_route is True:
            text_color = color['WHITE']

        distance_displayed = None
        if display_grid_color == mg_boundary.d_display_grid_color['TO_START_GRID'] \
                and self.distance is not None:
            distance_displayed = self.distance
        elif display_grid_color == mg_boundary.d_display_grid_color['TO_ROUTE'] \
                and self.distance_to_route != -1:
            distance_displayed = self.distance_to_route

        if distance_displayed is not None:
            text_surf, text_rect \
                = mg_function.textDisplay(str(int(distance_displayed)), "comicsansms",
                                          int(ceil(grid_size / 2)), text_color,
                                          grid_origin_pos_y + grid_size / 2, grid_origin_pos_x + grid_size / 2)
            display_surf.blit(text_surf, text_rect)

        return


    def display_wall_update(self, display_surf, origin_pos_x, origin_pos_y, grid_size):
        if self.status_changed is False:
            return

        # Allocate top left point
        grid_origin_pos_x = origin_pos_x + grid_size * self.pos_x
        grid_origin_pos_y = origin_pos_y + grid_size * self.pos_y

        # Draw walls
        wall_color = color['BLUE']
        if self.conn_to_up is False:
            pygame.draw.line(display_surf, wall_color, (grid_origin_pos_y, grid_origin_pos_x),
                             (grid_origin_pos_y + grid_size, grid_origin_pos_x),
                             mg_boundary.wall_thickness_pixel)
        if self.conn_to_left is False:
            pygame.draw.line(display_surf, wall_color, (grid_origin_pos_y, grid_origin_pos_x),
                             (grid_origin_pos_y, grid_origin_pos_x + grid_size),
                             mg_boundary.wall_thickness_pixel)

        return


# Advanced
class grid_data_objective:
    def __init__(self):
        # values for management
        self.id = None
        self.description = None
        self.active = None
        self.seen = None
        self.seed = None
        self.flag = None

        return

class grid_data_natural:
    def __init__(self):
        # short-term static
        self.plate = None
        self.temperature = None
        self.humidity = None
        self.altitude = None
        self.climate = None
        self.terrain = None

        # dynamic
        self.weather = None
        self.disaster = None
        self.resource = None
        self.vegetation = None
        self.animal = None

        return

class grid_data_artificial:
    def __init__(self):
        # short-term static
        self.name = None
        self.continent = None

        # dynamic
        self.population = None
        self.faction = None
        self.ideology = None
        self.belief = None
        self.development = None
        self.event = None
        self.celebrity = None
        self.history = None

        return

class grid_data:
    def __init__(self):
        self.objective = None
        self.natural = None
        self.artificial = None

        return

class adv_grid_2d_square:
    def __init__(self, x, y):
        # pos for position
        self.pos_x = x
        self.pos_y = y

        # nb for neighbor
        self.nb_up = None
        self.nb_down = None
        self.nb_left = None
        self.nb_right = None
        self.conn_to_up = False
        self.conn_to_left = False

        # data
        self.data = None

        return

class adv_grid_2d_hexagon:
    def __init__(self, x, y):
        # pos for position
        self.pos_x = x
        self.pos_y = y

        # nb for neighbor
        self.nb_up_left = None
        self.nb_up_right = None
        self.nb_down_left = None
        self.nb_down_right = None
        self.nb_left = None
        self.nb_right = None
        self.conn_to_up_left = False
        self.conn_to_down_left = False
        self.conn_to_left = False

        # data
        self.data = None

        return


# Wall of the Map
class improved_wall_2d_square:
    def __init__(self, grid_low, grid_high, direction, connection):
        # 0 for horizontal, 1 for vertical
        self.direction = direction

        # Low for up and left, high for down and right
        self.nb_grid_low = grid_low
        self.nb_grid_high = grid_high
        if direction == 0:
            grid_low.wall_down = self
            grid_high.wall_up = self
        elif direction == 1:
            grid_low.wall_right = self
            grid_high.wall_left = self

        self.existence = bool(1 - connection)

        return


# Area of the Map
class improved_area_2d_square:
    def __init__(self, index, map):
        self.area_index = index
        self.area_map = map
        self.grid_list = list()
        self.start_grid = list()
        self.route = list()
        self.border_grid_list = list()

        return


# Map
# Basic
class basic_map_2d_square:
    def __init__(self, m, n):
        # Size
        self.row_num = m
        self.column_num = n
        self.display_pos_set = (0, 0, 1280, 640)

        # Management
        self.num_nothing = m * n
        self.num_newborn = 0
        self.num_growing = 0
        self.num_mature = 0
        self.num_graven = 0
        self.generation_done = False
        self.entrance = None
        self.exit = None
        self.start_grid = list()
        self.route = list()

        # Grid list
        self.grid_list = [list() for i in range(m + 2)]

        return


    def gridInit(self):
        self.grid_list[0].append(basic_grid_2d_square(0, 0, None, None))
        for i in range(1, self.row_num + 2):
            self.grid_list[i].append(basic_grid_2d_square(i, 0, self.grid_list[i - 1][0], None))
        for j in range(1, self.column_num + 2):
            self.grid_list[0].append(basic_grid_2d_square(0, j, None, self.grid_list[0][j - 1]))
        for i in range(1, self.row_num + 2):
            for j in range(1, self.column_num + 2):
                self.grid_list[i].append(basic_grid_2d_square(i, j, self.grid_list[i - 1][j], self.grid_list[i][j - 1]))

        return


    def displayClearAll(self, display_surf):
        display_surf.fill(color['BLACK'])

        return


    def display(self, display_surf, origin_pos_x, origin_pos_y, grid_size):
        color_gradient = ceil(255 / (self.row_num + self.column_num) / 2 *sqrt(self.start_grid.__len__()))
        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                curr_grid.display_floor(display_surf, origin_pos_x, origin_pos_y, color_gradient, grid_size)
        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                curr_grid.display_wall(display_surf, origin_pos_x, origin_pos_y, grid_size)
        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                curr_grid.display_distance(display_surf, origin_pos_x, origin_pos_y, grid_size)

        return


    def displayWallOnly(self, display_surf, origin_pos_x, origin_pos_y, grid_size):
        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                curr_grid.display_wall(display_surf, origin_pos_x, origin_pos_y, grid_size)

        return


    def setBorder(self, mask):
        # Mask size has to be not larger than the size of the map in row and column
        # Or to say, only top-left part within that size limit is used
        for i in range(self.row_num):
            if i >= mask.__len__():
                break
            for j in range(self.column_num):
                if j >= mask[i].__len__():
                    break
                if mask[i][j] == 0:
                    self.grid_list[i + 1][j + 1].status = status.NEWBORN
                    self.num_newborn += 1
                    self.num_nothing -= 1

        # Left and right column
        for i in range(self.row_num + 2):
            self.grid_list[i][0].conn_to_up = True
            self.grid_list[i][0].conn_to_left = True
            self.grid_list[i][self.column_num + 1].conn_to_up = True

        # Top and bottom row
        for j in range(self.column_num + 2):
            self.grid_list[0][j].conn_to_up = True
            self.grid_list[0][j].conn_to_left = True
            self.grid_list[self.row_num + 1][j].conn_to_left = True

        # Main map
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.NOTHING:
                    if curr_grid.nb_up.status == status.NOTHING:
                        curr_grid.conn_to_up = True
                    if curr_grid.nb_down.status == status.NOTHING:
                        curr_grid.nb_down.conn_to_up = True
                    if curr_grid.nb_left.status == status.NOTHING:
                        curr_grid.conn_to_left = True
                    if curr_grid.nb_right.status == status.NOTHING:
                        curr_grid.nb_right.conn_to_left = True

        return


    def setEntranceAndExitGrid(self, entrance_nothing, entrance_newborn, exit_nothing, exit_newborn):
        if entrance_nothing == exit_nothing and entrance_newborn == exit_newborn:
            return

        # Either entrance or exit have to be NEWBORN and has an adjacent NOTHING
        curr_nothing = self.grid_list[entrance_nothing[0]][entrance_nothing[1]]
        curr_newborn = self.grid_list[entrance_newborn[0]][entrance_newborn[1]]
        self.entrance = curr_newborn
        if curr_nothing.nb_up == curr_newborn:
            curr_nothing.conn_to_up = True
        elif curr_nothing.nb_down == curr_newborn:
            curr_newborn.conn_to_up = True
        elif curr_nothing.nb_left == curr_newborn:
            curr_nothing.conn_to_left = True
        elif curr_nothing.nb_right == curr_newborn:
            curr_newborn.conn_to_left = True

        curr_nothing = self.grid_list[exit_nothing[0]][exit_nothing[1]]
        curr_newborn = self.grid_list[exit_newborn[0]][exit_newborn[1]]
        self.exit = curr_newborn
        if curr_nothing.nb_up == curr_newborn:
            curr_nothing.conn_to_up = True
        elif curr_nothing.nb_down == curr_newborn:
            curr_newborn.conn_to_up = True
        elif curr_nothing.nb_left == curr_newborn:
            curr_nothing.conn_to_left = True
        elif curr_nothing.nb_right == curr_newborn:
            curr_newborn.conn_to_left = True

        return


    def randomEntranceAndExitGrid(self):
        # Crack two random walls between NOTHING and NEWBORN
        wall_list = list()
        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                if curr_grid.status == status.NOTHING:
                    if curr_grid.nb_up is not None and curr_grid.nb_up.status == status.NEWBORN:
                        wall_list.append([curr_grid, curr_grid.nb_up])
                    if curr_grid.nb_down is not None and curr_grid.nb_down.status == status.NEWBORN:
                        wall_list.append([curr_grid, curr_grid.nb_down])
                    if curr_grid.nb_left is not None and curr_grid.nb_left.status == status.NEWBORN:
                        wall_list.append([curr_grid, curr_grid.nb_left])
                    if curr_grid.nb_right is not None and curr_grid.nb_right.status == status.NEWBORN:
                        wall_list.append([curr_grid, curr_grid.nb_right])

        index_list = mg_function.randomSampling(wall_list.__len__(), 2)
        for index in index_list:
            curr_grid = wall_list[index][0]
            curr_nb = wall_list[index][1]
            if curr_grid.nb_up == curr_nb:
                curr_grid.conn_to_up = True
            elif curr_grid.nb_down == curr_nb:
                curr_grid.nb_down.conn_to_up = True
            elif curr_grid.nb_left == curr_nb:
                curr_grid.conn_to_left = True
            elif curr_grid.nb_right == curr_nb:
                curr_grid.nb_right.conn_to_left = True
            else:
                break

        entrance_index = mg_function.randomSampling(2, 1)
        self.entrance = wall_list[index_list[entrance_index[0]]][1]
        self.exit = wall_list[index_list[1 - entrance_index[0]]][1]

        return


    def setGeneretionStartGrid(self, start_grid_list):
        for start_grid in start_grid_list:
            curr_grid = self.grid_list[start_grid[0], start_grid[1]]
            self.start_grid.append(curr_grid)
            curr_grid.status = status.MATURE
            curr_grid.distance = 0
            self.num_newborn -= 1
            self.num_mature += 1

        return


    def randomGenerationStartGrid(self, k):
        # Count avaliable grids
        num_grid = 0
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.NEWBORN:
                    num_grid += 1

        # Sampling start grids
        index_list = mg_function.randomSampling(num_grid, k)
        index = 0
        num_grid = 0

        # Set status to GROWING
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.NEWBORN:
                    if index_list[index] == num_grid:
                        self.start_grid.append(curr_grid)
                        curr_grid.status = status.MATURE
                        curr_grid.distance = 0
                        self.num_newborn -= 1
                        self.num_mature += 1
                        index += 1
                    num_grid += 1
                    if index == index_list.__len__():
                        return

        return


    def crackAWallForNewMature(self, curr_grid):
        # List neighbor MATURE grids
        nb_mature_list = list()
        if curr_grid.nb_up.status == status.MATURE:
            nb_mature_list.append(curr_grid.nb_up)
        if curr_grid.nb_down.status == status.MATURE:
            nb_mature_list.append(curr_grid.nb_down)
        if curr_grid.nb_left.status == status.MATURE:
            nb_mature_list.append(curr_grid.nb_left)
        if curr_grid.nb_right.status == status.MATURE:
            nb_mature_list.append(curr_grid.nb_right)

        # Pick one to connect
        nb_list = mg_function.randomSampling(nb_mature_list.__len__(), 1)
        if nb_list == list():
            return None

        # Remove the wall by setting connection to True
        nb = nb_mature_list[nb_list[0]]
        if nb == curr_grid.nb_up:
            curr_grid.conn_to_up = True
        elif nb == curr_grid.nb_down:
            curr_grid.nb_down.conn_to_up = True
        elif nb == curr_grid.nb_left:
            curr_grid.conn_to_left = True
        elif nb == curr_grid.nb_right:
            curr_grid.nb_right.conn_to_left = True

        return nb


    def growFromGrowingToMature(self, ratio):
        # List all GROWING
        growing_list = list()
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.GROWING:
                    growing_list.append(curr_grid)

        # Sampling new MATURE
        index_list = mg_function.randomSampling(growing_list.__len__(), ceil(growing_list.__len__() * ratio))

        # List new MATURE, do not set status here, or you may get unconnected area
        index = 0
        new_mature_list = list()

        if index_list == list():
            return
        for i in range(growing_list.__len__()):
            if i == index_list[index]:
                new_mature_list.append(growing_list[i])
                index += 1
                if index == index_list.__len__():
                    break

        # Random ordering new MATURE list
        index_list = mg_function.randomSequence(new_mature_list.__len__())

        # Break wall for new MATURE and set status
        for i in range(new_mature_list.__len__()):
            curr_grid = new_mature_list[index_list[i]]
            parent_grid = self.crackAWallForNewMature(curr_grid)
            curr_grid.distance = parent_grid.distance + 1
            curr_grid.status = status.MATURE
            self.num_growing -= 1
            self.num_mature += 1

        return


    def growFromNewbornToGrowing(self):
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.NEWBORN:
                    if curr_grid.nb_up.status == status.MATURE \
                            or curr_grid.nb_down.status == status.MATURE \
                            or curr_grid.nb_left.status == status.MATURE \
                            or curr_grid.nb_right.status == status.MATURE:
                        curr_grid.status = status.GROWING
                        self.num_newborn -= 1
                        self.num_growing += 1

        return


    def growFromMatureToGraven(self):
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.MATURE:
                    if curr_grid.nb_up.status != status.GROWING \
                            and curr_grid.nb_down.status != status.GROWING \
                            and curr_grid.nb_left.status != status.GROWING \
                            and curr_grid.nb_right.status != status.GROWING:
                        curr_grid.status = status.GRAVEN
                        self.num_mature -= 1
                        self.num_graven += 1

        return


    def isGrenerationDone(self):
        if self.num_newborn == 0 and self.num_growing == 0 and self.num_mature == 0:
            self.generation_done = True

        return


    def growOneRound(self, ratio):
        self.growFromNewbornToGrowing()
        self.growFromMatureToGraven()
        self.growFromGrowingToMature(ratio)
        self.isGrenerationDone()

        return


    def calculateDistance(self, x, y):
        # No need to use a function, set distance when crack wall
        calculate_done = False
        next_list = list()
        next_list.append(self.grid_list[x][y])
        curr_distance = 0
        while calculate_done is False:
            curr_list = next_list.copy()
            next_list = list()
            for curr_grid in curr_list:
                curr_grid.distance = curr_distance
                if curr_grid.nb_up.distance is None \
                        and curr_grid.nb_up.status == status.GRAVEN and curr_grid.conn_to_up is True:
                    next_list.append(curr_grid.nb_up)
                if curr_grid.nb_down.distance is None \
                        and curr_grid.nb_down.status == status.GRAVEN and curr_grid.nb_down.conn_to_up is True:
                    next_list.append(curr_grid.nb_down)
                if curr_grid.nb_left.distance is None \
                        and curr_grid.nb_left.status == status.GRAVEN and curr_grid.conn_to_left is True:
                    next_list.append(curr_grid.nb_left)
                if curr_grid.nb_right.distance is None \
                        and curr_grid.nb_right.status == status.GRAVEN and curr_grid.nb_right.conn_to_left is True:
                    next_list.append(curr_grid.nb_right)
            if next_list == list():
                calculate_done = True
            else:
                curr_distance += 1

        return


    def findRouteToStartGrid(self, grid):
        route_list = list()
        curr_grid = grid
        while curr_grid != self.start_grid[0]:
            route_list.append(curr_grid)
            if curr_grid.conn_to_up is True and curr_grid.nb_up.distance is not None \
                    and curr_grid.distance == curr_grid.nb_up.distance + 1:
                curr_grid = curr_grid.nb_up
            elif curr_grid.nb_down.conn_to_up is True and curr_grid.nb_down.distance is not None \
                    and curr_grid.distance == curr_grid.nb_down.distance + 1:
                curr_grid = curr_grid.nb_down
            elif curr_grid.conn_to_left is True and curr_grid.nb_left.distance is not None \
                    and curr_grid.distance == curr_grid.nb_left.distance + 1:
                curr_grid = curr_grid.nb_left
            elif curr_grid.nb_right.conn_to_left is True and curr_grid.nb_right.distance is not None \
                    and curr_grid.distance == curr_grid.nb_right.distance + 1:
                curr_grid = curr_grid.nb_right
            else:
                break
        route_list.append(curr_grid)

        return route_list


    def findSingleStartGridRoute(self):
        # start_grid_num == 1
        self.route = self.findRouteToStartGrid(self.entrance)
        route_exit = self.findRouteToStartGrid(self.exit)
        for i in range(route_exit.__len__()):
            if self.route.__len__() > 1 and route_exit.__len__() > i + 1 \
                    and self.route[-2] == route_exit[-i - 2]:
                self.route.pop()
            elif self.route[-1] != route_exit[-i - 1]:
                self.route.append(route_exit[-i - 1])

        for curr_grid in self.route:
            curr_grid.on_route = True

        return


# Improved
class improved_map_2d_square(basic_map_2d_square):
    def __init__(self, m, n, display_grid_color, display_grid_distance, display_route):
        # Inherit
        basic_map_2d_square.__init__(self, m, n)

        # Improved
        # Horizontal walls (m + 1) * (n + 2)
        self.wall_list_h = [list() for i in range(m + 1)]
        # Vertical walls (m + 2) * (n + 1)
        self.wall_list_v = [list() for i in range(m + 2)]
        self.connection_matrix = None
        self.distance_matrix = None
        self.area_num = 0
        self.area_route = None
        self.entrance_list = list()
        self.exit_list = list()
        self.display_grid_color = display_grid_color
        self.display_grid_distance = display_grid_distance
        self.display_route = display_route
        self.turns_on_route = 0
        self.average_distance_to_route = 0
        self.max_distance_to_route = 0

        return


    def improvedGridInit(self):
        self.grid_list[0].append(improved_grid_2d_square(0, 0, None, None))
        for i in range(1, self.row_num + 2):
            self.grid_list[i].append(improved_grid_2d_square(i, 0, self.grid_list[i - 1][0], None))
        for j in range(1, self.column_num + 2):
            self.grid_list[0].append(improved_grid_2d_square(0, j, None, self.grid_list[0][j - 1]))
        for i in range(1, self.row_num + 2):
            for j in range(1, self.column_num + 2):
                self.grid_list[i].append(improved_grid_2d_square(i, j, self.grid_list[i - 1][j], self.grid_list[i][j - 1]))

        return


    def initWallLists(self):
        for i in range(1, self.row_num + 2):
            for j in range(self.column_num + 2):
                self.wall_list_h[i - 1].append(improved_wall_2d_square(self.grid_list[i - 1][j], self.grid_list[i][j],
                                                                       0, self.grid_list[i][j].conn_to_up))
        for i in range(self.row_num + 2):
            for j in range(1, self.column_num + 2):
                self.wall_list_v[i].append(improved_wall_2d_square(self.grid_list[i][j - 1], self.grid_list[i][j],
                                                                   1, self.grid_list[i][j].conn_to_left))

        return


    def updateWallLists(self):
        for i in range(1, self.row_num + 2):
            for j in range(self.column_num + 2):
                self.wall_list_h[i - 1].append(improved_wall_2d_square(self.grid_list[i - 1][j], self.grid_list[i][j],
                                                                       0, self.grid_list[i][j].conn_to_up))
        for i in range(self.row_num + 2):
            for j in range(1, self.column_num + 2):
                self.wall_list_v[i].append(improved_wall_2d_square(self.grid_list[i][j - 1], self.grid_list[i][j],
                                                                   1, self.grid_list[i][j].conn_to_left))

        return


    def updateConnectionMatrix(self):
        for wall_list_h_row in self.wall_list_h:
            for wall in wall_list_h_row:
                nb_high = wall.nb_grid_high
                nb_low = wall.nb_grid_low
                if nb_high.connected_area != nb_low.connected_area:
                    self.connection_matrix[nb_high.connected_area][nb_low.connected_area] = 1
                    self.connection_matrix[nb_low.connected_area][nb_high.connected_area] = 1
                    if nb_high.distance is None:
                        distance = nb_low.distance
                    elif nb_low.distance is None:
                        distance = nb_high.distance
                    else:
                        distance = nb_high.distance + nb_low.distance
                    if distance > self.distance_matrix[nb_high.connected_area][nb_low.connected_area]:
                        self.distance_matrix[nb_high.connected_area][nb_low.connected_area] = distance
                        self.distance_matrix[nb_low.connected_area][nb_high.connected_area] = distance
        for wall_list_v_row in self.wall_list_v:
            for wall in wall_list_v_row:
                nb_high = wall.nb_grid_high
                nb_low = wall.nb_grid_low
                if nb_high.connected_area != nb_low.connected_area:
                    self.connection_matrix[nb_high.connected_area][nb_low.connected_area] = 1
                    self.connection_matrix[nb_low.connected_area][nb_high.connected_area] = 1
                    if nb_high.distance is None:
                        distance = nb_low.distance
                    elif nb_low.distance is None:
                        distance = nb_high.distance
                    else:
                        distance = nb_high.distance + nb_low.distance
                    if distance > self.distance_matrix[nb_high.connected_area][nb_low.connected_area]:
                        self.distance_matrix[nb_high.connected_area][nb_low.connected_area] = distance
                        self.distance_matrix[nb_low.connected_area][nb_high.connected_area] = distance

        print(self.connection_matrix)
        print(self.distance_matrix)

        return


    def displayClearMap(self, display_surf):
        pygame.draw.rect(display_surf, color['BLACK'], self.display_pos_set)

        return


    def update_display_settings(self, display_grid_color, display_grid_distance, display_route):
        self.display_grid_color = display_grid_color
        self.display_grid_distance = display_grid_distance
        self.display_route = display_route

        return


    def set_all_update_flag(self, flag):
        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                curr_grid.status_changed = flag

        return


    def display_update(self, display_surf, origin_pos_x, origin_pos_y, grid_size):
        display_grid_color = self.display_grid_color
        display_grid_distance = self.display_grid_distance
        display_route = self.display_route
        if self.display_grid_color == mg_boundary.d_display_grid_color['TO_START_GRID']:
            color_gradient \
                = ceil(255 / sqrt(self.row_num * self.column_num) / 2 * sqrt(self.start_grid.__len__()))
        else:
            color_gradient \
                = ceil(255 / sqrt(self.row_num * self.column_num) * sqrt(self.start_grid.__len__()))

        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                curr_grid.display_floor_update(display_surf, origin_pos_x, origin_pos_y, color_gradient, grid_size,
                                               display_grid_color)
        for grid_list_row in self.grid_list:
            for curr_grid in grid_list_row:
                curr_grid.display_wall_update(display_surf, origin_pos_x, origin_pos_y, grid_size)
        if display_grid_distance is True:
            for grid_list_row in self.grid_list:
                for curr_grid in grid_list_row:
                    curr_grid.display_distance_update(display_surf, origin_pos_x, origin_pos_y, grid_size,
                                                      display_grid_color, display_route)

        self.set_all_update_flag(False)

        return


    def improvedSetGeneretionStartGrid(self, start_grid_list):
        area_num = 0
        for start_grid in start_grid_list:
            curr_grid = self.grid_list[start_grid[0], start_grid[1]]
            if curr_grid.status != status.NEWBORN:
                continue
            self.start_grid.append(curr_grid)
            curr_grid.status = status.MATURE
            curr_grid.distance = 0
            curr_grid.connected_area = area_num + 1
            self.num_newborn -= 1
            self.num_mature += 1
            area_num += 1

        # Add entrance and exit grids
        if self.entrance is not None and self.exit is not None:
            if self.entrance.connected_area == 0:
                curr_grid = self.entrance
                self.start_grid.append(curr_grid)
                curr_grid.status = status.MATURE
                curr_grid.distance = 0
                curr_grid.connected_area = area_num + 1
                self.num_newborn -= 1
                self.num_mature += 1
                area_num += 1
            if self.exit.connected_area == 0:
                curr_grid = self.exit
                self.start_grid.append(curr_grid)
                curr_grid.status = status.MATURE
                curr_grid.distance = 0
                curr_grid.connected_area = area_num + 1
                self.num_newborn -= 1
                self.num_mature += 1
                area_num += 1

        self.connection_matrix = zeros((area_num + 1, area_num + 1))
        self.distance_matrix = -ones((area_num + 1, area_num + 1))
        self.area_num = area_num

        return


    def improvedRandomGenerationStartGrid(self, area_num):
        # Count available grids
        num_grid = 0
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.NEWBORN:
                    num_grid += 1

        # Sampling start grids
        index_list = mg_function.randomSampling(num_grid, area_num)
        index = 0
        num_grid = 0

        # Set status to MATURE
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.NEWBORN:
                    if index_list[index] == num_grid:
                        self.start_grid.append(curr_grid)
                        curr_grid.status = status.MATURE
                        curr_grid.distance = 0
                        curr_grid.connected_area = index + 1
                        self.num_newborn -= 1
                        self.num_mature += 1
                        index += 1
                    num_grid += 1
                    if index == area_num:
                        break
            if index == area_num:
                break

        # To avoid entrance and exit exist in the same area, replace first two start grids with them if they are decided
        # If only one area, or to say, single start grid mode, skip this step
        #print(self.start_grid)
        #print(self.entrance)
        #print(self.exit)
        if area_num != 1:
            if self.entrance is not None and self.entrance not in self.start_grid:
                if self.start_grid[0] != self.exit:
                    self.start_grid[0].status = status.NEWBORN
                    self.start_grid[0].distance = None
                    self.start_grid[0].connected_area = 0
                    self.entrance.status = status.MATURE
                    self.entrance.distance = 0
                    self.entrance.connected_area = 1
                    self.start_grid[0] = self.entrance
                else:
                    self.start_grid[1].status = status.NEWBORN
                    self.start_grid[1].distance = None
                    self.start_grid[1].connected_area = 0
                    self.entrance.status = status.MATURE
                    self.entrance.distance = 0
                    self.entrance.connected_area = 2
                    self.start_grid[1] = self.entrance
            if self.exit is not None and self.exit not in self.start_grid:
                if self.start_grid[1] != self.entrance:
                    self.start_grid[1].status = status.NEWBORN
                    self.start_grid[1].distance = None
                    self.start_grid[1].connected_area = 0
                    self.exit.status = status.MATURE
                    self.exit.distance = 0
                    self.exit.connected_area = 2
                    self.start_grid[1] = self.exit
                else:
                    self.start_grid[0].status = status.NEWBORN
                    self.start_grid[0].distance = None
                    self.start_grid[0].connected_area = 0
                    self.exit.status = status.MATURE
                    self.exit.distance = 0
                    self.exit.connected_area = 1
                    self.start_grid[0] = self.exit

        # Init connection matrix
        self.connection_matrix = zeros((area_num + 1, area_num + 1))
        self.distance_matrix = -ones((area_num + 1, area_num + 1))
        self.area_num = area_num

        return


    def improvedSetEntranceAndExitGrid(self, entrance_out, entrance_in, exit_out, exit_in):
        if entrance_out == exit_out and entrance_in == exit_in:
            return

        # Either entrance or exit have to be NEWBORN(in) and has an adjacent NOTHING(out)
        curr_out = self.grid_list[entrance_out[0]][entrance_out[1]]
        curr_in = self.grid_list[entrance_in[0]][entrance_in[1]]
        self.entrance = curr_in
        if curr_out.nb_up == curr_in:
            curr_out.conn_to_up = True
        elif curr_out.nb_down == curr_in:
            curr_in.conn_to_up = True
        elif curr_out.nb_left == curr_in:
            curr_out.conn_to_left = True
        elif curr_out.nb_right == curr_in:
            curr_in.conn_to_left = True

        curr_out = self.grid_list[exit_out[0]][exit_out[1]]
        curr_in = self.grid_list[exit_in[0]][exit_in[1]]
        self.exit = curr_in
        if curr_out.nb_up == curr_in:
            curr_out.conn_to_up = True
        elif curr_out.nb_down == curr_in:
            curr_in.conn_to_up = True
        elif curr_out.nb_left == curr_in:
            curr_out.conn_to_left = True
        elif curr_out.nb_right == curr_in:
            curr_in.conn_to_left = True

        return


    def improvedRandomEntranceAndExitGrid(self):
        # Crack two random walls between NOTHING and NEWBORN
        wall_list = list()
        for wall_list_h_row in self.wall_list_h:
            for curr_wall in wall_list_h_row:
                if curr_wall.nb_grid_high.status == status.NOTHING and curr_wall.nb_grid_low.status != status.NOTHING:
                    wall_list.append(curr_wall)
                if curr_wall.nb_grid_high.status != status.NOTHING and curr_wall.nb_grid_low.status == status.NOTHING:
                    wall_list.append(curr_wall)
        for wall_list_v_row in self.wall_list_v:
            for curr_wall in wall_list_v_row:
                if curr_wall.nb_grid_high.status == status.NOTHING and curr_wall.nb_grid_low.status != status.NOTHING:
                    wall_list.append(curr_wall)
                if curr_wall.nb_grid_high.status != status.NOTHING and curr_wall.nb_grid_low.status == status.NOTHING:
                    wall_list.append(curr_wall)

        while True:
            index_list = mg_function.randomSampling(wall_list.__len__(), 2)
            print(index_list)

            curr_wall_0 = wall_list[index_list[0]]
            curr_wall_1 = wall_list[index_list[1]]
            if curr_wall_0.nb_grid_low.status == status.NOTHING:
                curr_internal_grid_0 = curr_wall_0.nb_grid_high
            else:
                curr_internal_grid_0 = curr_wall_0.nb_grid_low
            if curr_wall_1.nb_grid_low.status == status.NOTHING:
                curr_internal_grid_1 = curr_wall_1.nb_grid_high
            else:
                curr_internal_grid_1 = curr_wall_1.nb_grid_low

            if curr_internal_grid_0 != curr_internal_grid_1:
                break

        for index in index_list:
            curr_wall = wall_list[index]
            curr_wall.existence = False
            if curr_wall.direction == 1:
                curr_wall.nb_grid_high.conn_to_left = True
            else:
                curr_wall.nb_grid_high.conn_to_up = True

        entrance_index = mg_function.randomSampling(2, 1)

        curr_wall = wall_list[index_list[entrance_index[0]]]
        if curr_wall.nb_grid_low.status == status.NOTHING:
            self.entrance = curr_wall.nb_grid_high
        else:
            self.entrance = curr_wall.nb_grid_low

        curr_wall = wall_list[index_list[1 - entrance_index[0]]]
        if curr_wall.nb_grid_low.status == status.NOTHING:
            self.exit = curr_wall.nb_grid_high
        else:
            self.exit = curr_wall.nb_grid_low

        return


    def improvedGrowFromGrowingToMature(self, ratio):
        # List all GROWING
        growing_list = list()
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.GROWING:
                    growing_list.append(curr_grid)

        # Sampling new MATURE
        index_list = mg_function.randomSampling(growing_list.__len__(), ceil(growing_list.__len__() * ratio))

        # List new MATURE, do not set status here, or you may get unconnected area
        index = 0
        new_mature_list = list()

        if index_list == list():
            return
        for i in range(growing_list.__len__()):
            if i == index_list[index]:
                new_mature_list.append(growing_list[i])
                index += 1
                if index == index_list.__len__():
                    break

        # Random ordering new MATURE list
        index_list = mg_function.randomSequence(new_mature_list.__len__())

        # Break wall for new MATURE and set status
        for i in range(new_mature_list.__len__()):
            curr_grid = new_mature_list[index_list[i]]
            parent_grid = self.crackAWallForNewMature(curr_grid)
            curr_grid.distance = parent_grid.distance + 1
            curr_grid.connected_area = parent_grid.connected_area
            curr_grid.status = status.MATURE
            curr_grid.status_changed = True
            self.num_growing -= 1
            self.num_mature += 1

        return


    def improvedGrowFromNewbornToGrowing(self):
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.NEWBORN:
                    if curr_grid.nb_up.status == status.MATURE \
                            or curr_grid.nb_down.status == status.MATURE \
                            or curr_grid.nb_left.status == status.MATURE \
                            or curr_grid.nb_right.status == status.MATURE:
                        curr_grid.status = status.GROWING
                        curr_grid.status_changed = True
                        self.num_newborn -= 1
                        self.num_growing += 1

        return


    def improvedGrowFromMatureToGraven(self):
        for grid_list_row in self.grid_list[1 : self.row_num + 1]:
            for curr_grid in grid_list_row[1 : self.column_num + 1]:
                if curr_grid.status == status.MATURE:
                    if curr_grid.nb_up.status != status.GROWING \
                            and curr_grid.nb_down.status != status.GROWING \
                            and curr_grid.nb_left.status != status.GROWING \
                            and curr_grid.nb_right.status != status.GROWING:
                        curr_grid.status = status.GRAVEN
                        curr_grid.status_changed = True
                        self.num_mature -= 1
                        self.num_graven += 1

        return


    def improvedGrowOneRound(self, ratio):
        self.improvedGrowFromNewbornToGrowing()
        self.improvedGrowFromMatureToGraven()
        self.improvedGrowFromGrowingToMature(ratio)
        self.isGrenerationDone()

        return


    def findLargestAreaRoute(self):
        # Entrance and exit fixed, remove connection between border and other areas
        # If there is only one area, as known as, single start grid mode, skip this step.
        if self.entrance is not None and self.exit is not None and self.area_num != 1:
            for i in range(self.connection_matrix.__len__()):
                if self.connection_matrix[0][i] != 0:
                    if self.entrance.connected_area == i:
                        self.connection_matrix[i][0] = 0
                        self.distance_matrix[i][0] = -1
                    elif self.exit.connected_area == i:
                        self.connection_matrix[0][i] = 0
                        self.distance_matrix[0][i] = -1
                    else:
                        self.connection_matrix[0][i] = 0
                        self.connection_matrix[i][0] = 0
                        self.distance_matrix[0][i] = -1
                        self.distance_matrix[i][0] = -1

        # Generate the area route
        self.area_route = mg_function.findLargestRouteWithoutOverlap(self.connection_matrix)
        print('work_count: ' + str(mg_function.work_count))

        return


    def findLongestAreaRoute(self):
        # Entrance and exit fixed, remove connection between border and other areas
        # If there is only one area, as known as, single start grid mode, skip this step.
        if self.entrance is not None and self.exit is not None and self.area_num != 1:
            print(self.entrance.connected_area)
            print(self.exit.connected_area)
            for i in range(self.connection_matrix.__len__()):
                if self.connection_matrix[0][i] != 0:
                    if self.entrance.connected_area == i:
                        self.connection_matrix[i][0] = 0
                        self.distance_matrix[i][0] = -1
                    elif self.exit.connected_area == i:
                        self.connection_matrix[0][i] = 0
                        self.distance_matrix[0][i] = -1
                    else:
                        self.connection_matrix[0][i] = 0
                        self.connection_matrix[i][0] = 0
                        self.distance_matrix[0][i] = -1
                        self.distance_matrix[i][0] = -1

        # Generate the area route
        self.area_route = mg_function.findLongestRouteWithoutOverlap(self.distance_matrix)
        print('work_count: ' + str(mg_function.work_count))

        return


    def breakOneWallForEachAreaNotInAreaRoute(self):
        # Break the wall to an area on route first
        desert_area = list()
        for i in range(1, self.area_num + 1):
            if i not in self.area_route:
                desert_area.append(i)

        print(self.area_route)
        print(desert_area)

        while desert_area.__len__() != 0:
            edge = list()
            index = 0
            break_flag = 0
            while break_flag == 0:
                area = desert_area[index]
                for i in range(1, self.area_num + 1):
                    if self.connection_matrix[i][area] and i not in desert_area:
                        break_flag = 1
                index += 1

            for wall_list_h_row in self.wall_list_h:
                for wall in wall_list_h_row:
                    if wall.nb_grid_low.connected_area == area \
                            and wall.nb_grid_high.connected_area not in desert_area \
                            and wall.nb_grid_high.connected_area != 0:
                        edge.append(wall)
                    elif wall.nb_grid_low.connected_area not in desert_area \
                            and wall.nb_grid_high.connected_area == area \
                            and wall.nb_grid_low.connected_area != 0:
                        edge.append(wall)
            for wall_list_v_row in self.wall_list_v:
                for wall in wall_list_v_row:
                    if wall.nb_grid_low.connected_area == area \
                            and wall.nb_grid_high.connected_area not in desert_area \
                            and wall.nb_grid_high.connected_area != 0:
                        edge.append(wall)
                    elif wall.nb_grid_low.connected_area not in desert_area \
                            and wall.nb_grid_high.connected_area == area \
                            and wall.nb_grid_low.connected_area != 0:
                        edge.append(wall)

            wall_index = mg_function.randomSampling(edge.__len__(), 1)
            curr_wall = edge[wall_index[0]]
            curr_wall.existence = False
            if curr_wall.direction == 0:
                curr_wall.nb_grid_high.conn_to_up = True
            elif curr_wall.direction == 1:
                curr_wall.nb_grid_high.conn_to_left = True

            desert_area.pop(index - 1)

        return


    def generateRandomEntranceAndExitGrids(self):
        # Break one wall for each area not in area route
        self.breakOneWallForEachAreaNotInAreaRoute()

        # Break one wall for each area not in area route
        for i in range(1, self.area_num + 1):
            if i not in self.area_route:
                edge = list()
                for wall_list_h_row in self.wall_list_h:
                    for wall in wall_list_h_row:
                        if wall.nb_grid_low.connected_area == i and wall.nb_grid_high.connected_area != 0:
                            edge.append(wall)
                        elif wall.nb_grid_low.connected_area != 0 and wall.nb_grid_high.connected_area == i:
                            edge.append(wall)
                for wall_list_v_row in self.wall_list_v:
                    for wall in wall_list_v_row:
                        if wall.nb_grid_low.connected_area == i and wall.nb_grid_high.connected_area != 0:
                            edge.append(wall)
                        elif wall.nb_grid_low.connected_area != 0 and wall.nb_grid_high.connected_area == i:
                            edge.append(wall)

                index = mg_function.randomSampling(edge.__len__(), 1)
                curr_wall = edge[index[0]]
                curr_wall.existence = False
                if curr_wall.direction == 0:
                    curr_wall.nb_grid_high.conn_to_up = True
                elif curr_wall.direction == 1:
                    curr_wall.nb_grid_high.conn_to_left = True

        # Break walls for other areas
        for i in range(self.area_route.__len__() - 1):
            area_index_low = self.area_route[i]
            area_index_high = self.area_route[i + 1]
            edge = list()

            # Break a random wall between two areas
            for wall_list_h_row in self.wall_list_h:
                for wall in wall_list_h_row:
                    if wall.nb_grid_low.connected_area == area_index_low \
                            and wall.nb_grid_high.connected_area == area_index_high:
                        edge.append(wall)
                    elif wall.nb_grid_low.connected_area == area_index_high \
                            and wall.nb_grid_high.connected_area == area_index_low:
                        edge.append(wall)
            for wall_list_v_row in self.wall_list_v:
                for wall in wall_list_v_row:
                    if wall.nb_grid_low.connected_area == area_index_low \
                            and wall.nb_grid_high.connected_area == area_index_high:
                        edge.append(wall)
                    elif wall.nb_grid_low.connected_area == area_index_high \
                            and wall.nb_grid_high.connected_area == area_index_low:
                        edge.append(wall)

            index = mg_function.randomSampling(edge.__len__(), 1)
            curr_wall = edge[index[0]]

            if curr_wall.nb_grid_low.connected_area == area_index_low:
                self.exit_list.append(curr_wall.nb_grid_low)
                self.entrance_list.append(curr_wall.nb_grid_high)
            elif curr_wall.nb_grid_low.connected_area == area_index_high:
                self.exit_list.append(curr_wall.nb_grid_high)
                self.entrance_list.append(curr_wall.nb_grid_low)

            if self.entrance is not None and self.entrance.connected_area == area_index_high:
                continue
            if self.exit is not None and self.exit.connected_area == area_index_low:
                continue

            curr_wall.existence = False
            if curr_wall.direction == 0:
                curr_wall.nb_grid_high.conn_to_up = True
            elif curr_wall.direction == 1:
                curr_wall.nb_grid_high.conn_to_left = True

        print(self.connection_matrix)
        print(self.area_route)

        self.exit_list.pop(0)
        self.entrance_list.pop()

        if self.entrance is not None:
            self.entrance_list[0] = self.entrance
        else:
            self.entrance = self.entrance_list[0]
        if self.exit is not None:
            self.exit_list[-1] = self.exit
        else:
            self.exit = self.exit_list[-1]

        return


    def wallQualification(self, wall, curr_distance, edge):
        if wall.nb_grid_high.distance is None:
            tmp_distance = wall.nb_grid_low.distance
        elif wall.nb_grid_low.distance is None:
            tmp_distance = wall.nb_grid_high.distance
        else:
            tmp_distance = wall.nb_grid_low.distance + wall.nb_grid_high.distance

        if tmp_distance == curr_distance:
            edge.append(wall)


    def generateLongestAreaRouteEntranceAndExitGrids(self):
        # Break one wall for each area not in area route
        self.breakOneWallForEachAreaNotInAreaRoute()

        # Break walls for other areas
        for i in range(self.area_route.__len__() - 1):
            area_index_low = self.area_route[i]
            area_index_high = self.area_route[i + 1]
            curr_distance = self.distance_matrix[area_index_low][area_index_high]
            edge = list()

            # Break the wall with the largest sum distance
            for wall_list_h_row in self.wall_list_h:
                for wall in wall_list_h_row:
                    if wall.nb_grid_low.connected_area == area_index_low \
                            and wall.nb_grid_high.connected_area == area_index_high:
                        self.wallQualification(wall, curr_distance, edge)
                    elif wall.nb_grid_low.connected_area == area_index_high \
                            and wall.nb_grid_high.connected_area == area_index_low:
                        self.wallQualification(wall, curr_distance, edge)
            for wall_list_v_row in self.wall_list_v:
                for wall in wall_list_v_row:
                    if wall.nb_grid_low.connected_area == area_index_low \
                            and wall.nb_grid_high.connected_area == area_index_high:
                        self.wallQualification(wall, curr_distance, edge)
                    elif wall.nb_grid_low.connected_area == area_index_high \
                            and wall.nb_grid_high.connected_area == area_index_low:
                        self.wallQualification(wall, curr_distance, edge)

            index = mg_function.randomSampling(edge.__len__(), 1)
            curr_wall = edge[index[0]]

            if curr_wall.nb_grid_low.connected_area == area_index_low:
                self.exit_list.append(curr_wall.nb_grid_low)
                self.entrance_list.append(curr_wall.nb_grid_high)
            elif curr_wall.nb_grid_low.connected_area == area_index_high:
                self.exit_list.append(curr_wall.nb_grid_high)
                self.entrance_list.append(curr_wall.nb_grid_low)

            if self.entrance is not None and self.entrance.connected_area == area_index_high:
                continue
            if self.exit is not None and self.exit.connected_area == area_index_low:
                continue

            curr_wall.existence = False
            if curr_wall.direction == 0:
                curr_wall.nb_grid_high.conn_to_up = True
            elif curr_wall.direction == 1:
                curr_wall.nb_grid_high.conn_to_left = True

        print(self.connection_matrix)

        self.exit_list.pop(0)
        self.entrance_list.pop()

        if self.entrance is not None:
            self.entrance_list[0] = self.entrance
        else:
            self.entrance = self.entrance_list[0]
        if self.exit is not None:
            self.exit_list[-1] = self.exit
        else:
            self.exit = self.exit_list[-1]

        return


    def improvedFindRouteToStartGrid(self, grid, start_grid):
        route_list = list()
        curr_grid = grid
        while curr_grid != start_grid:
            route_list.append(curr_grid)
            if curr_grid.conn_to_up is True and curr_grid.nb_up.distance is not None \
                    and curr_grid.connected_area == curr_grid.nb_up.connected_area \
                    and curr_grid.distance == curr_grid.nb_up.distance + 1:
                curr_grid = curr_grid.nb_up
            elif curr_grid.nb_down.conn_to_up is True and curr_grid.nb_down.distance is not None \
                    and curr_grid.connected_area == curr_grid.nb_down.connected_area \
                    and curr_grid.distance == curr_grid.nb_down.distance + 1:
                curr_grid = curr_grid.nb_down
            elif curr_grid.conn_to_left is True and curr_grid.nb_left.distance is not None \
                    and curr_grid.connected_area == curr_grid.nb_left.connected_area \
                    and curr_grid.distance == curr_grid.nb_left.distance + 1:
                curr_grid = curr_grid.nb_left
            elif curr_grid.nb_right.conn_to_left is True and curr_grid.nb_right.distance is not None \
                    and curr_grid.connected_area == curr_grid.nb_right.connected_area \
                    and curr_grid.distance == curr_grid.nb_right.distance + 1:
                curr_grid = curr_grid.nb_right
            else:
                break
        route_list.append(curr_grid)

        return route_list


    def findMultipleStartGridRoute(self):
        for i in range(self.entrance_list.__len__()):
            route_entrance = self.improvedFindRouteToStartGrid(self.entrance_list[i], self.start_grid[i])
            route_exit = self.improvedFindRouteToStartGrid(self.exit_list[i], self.start_grid[i])
            for j in range(route_exit.__len__()):
                if route_entrance.__len__() > 1 and route_exit.__len__() > j + 1 \
                        and route_entrance[-2] == route_exit[-j - 2]:
                    route_entrance.pop()
                elif route_entrance[-1] != route_exit[-j - 1]:
                    route_entrance.append(route_exit[-j - 1])

            self.route.extend(route_entrance)

        for curr_grid in self.route:
            curr_grid.on_route = True

        return


    def calculateTurnsOnRoute(self):
        self.turns_on_route = 0
        for i in range(self.route.__len__() - 2):
            if self.route[i]. pos_x != self.route[i + 2].pos_x and self.route[i]. pos_y != self.route[i + 2].pos_y:
                self.turns_on_route += 1

        return self.turns_on_route


    def calculateDistanceToRoute(self):
        sum_distance_to_route = 0
        calculated_grid_num = 0

        for curr_grid in self.route:
            curr_grid.distance_to_route = 0
            calculated_grid_num += 1

        if calculated_grid_num == 0:
            # Route is not generated yet.
            return -1

        remain_grid_num = -1
        curr_distance = 1
        while remain_grid_num != 0:
            print(remain_grid_num)
            remain_grid_num = 0
            for grid_list_row in self.grid_list[1 : self.row_num + 1]:
                for curr_grid in grid_list_row[1 : self.column_num + 1]:
                    if curr_grid.connected_area == 0 or curr_grid.distance_to_route != -1:
                        continue

                    if curr_grid.nb_up.distance_to_route != -1 \
                            and curr_grid.nb_up.distance_to_route != curr_distance\
                            and curr_grid.conn_to_up is True:
                        curr_grid.distance_to_route = curr_distance
                    if curr_grid.nb_down.distance_to_route != -1 \
                            and curr_grid.nb_down.distance_to_route != curr_distance\
                            and curr_grid.nb_down.conn_to_up is True:
                        curr_grid.distance_to_route = curr_distance
                    if curr_grid.nb_left.distance_to_route != -1 \
                            and curr_grid.nb_left.distance_to_route != curr_distance\
                            and curr_grid.conn_to_left is True:
                        curr_grid.distance_to_route = curr_distance
                    if curr_grid.nb_right.distance_to_route != -1 \
                            and curr_grid.nb_right.distance_to_route != curr_distance\
                            and curr_grid.nb_right.conn_to_left is True:
                        curr_grid.distance_to_route = curr_distance

                    if curr_grid.distance_to_route == -1:
                        remain_grid_num += 1
                    else:
                        sum_distance_to_route += curr_distance
                        calculated_grid_num += 1

            curr_distance += 1

        self.average_distance_to_route = sum_distance_to_route / calculated_grid_num
        self.max_distance_to_route = curr_distance - 1

        return self.average_distance_to_route, self.max_distance_to_route


# Output
class statistics_output:
    def __init__(self, description):
        self.description = description
        self.e2e_distance = 0
        self.sample_size = 0
        self.route_lenth = list()
        self.sum_route_lenth = 0
        self.sample_mean = 0
        self.lenth_to_distance = 0
        self.mean_squared_sum = 0
        self.sample_variance = 0
        self.standard_deviation = 0
        self.coefficient_of_variation = 0


    def add_one_sample(self, route_lenth):
        self.sample_size += 1
        self.route_lenth.append(route_lenth)
        self.sum_route_lenth += route_lenth

        return


    def update_e2e_distance(self, e2e_distance):
        self.e2e_distance = e2e_distance


    def calculate_statistics(self):
        self.sample_mean = self.sum_route_lenth / self.sample_size
        self.lenth_to_distance = self.sample_mean / self.e2e_distance
        for lenth in self.route_lenth:
            self.mean_squared_sum += pow((lenth - self.sample_mean), 2)
        self.sample_variance = self.mean_squared_sum / (self.sample_size - 1)
        self.standard_deviation = sqrt(self.sample_variance)
        self.coefficient_of_variation = self.standard_deviation / self.sample_mean

        return


    def dump_to_file(self, path, flag_clear_old):
        if flag_clear_old is True:
            output = open(path, 'w')
        elif flag_clear_old is False:
            output = open(path, 'a')
        else:
            return

        output.write(self.description + '\n')
        output.write('size: \t' + str(self.sample_size)
                     + '\t\t' + 'mean: \t' + str(self.sample_mean)
                     + '\t\t' + 'variance: \t' + str(self.sample_variance)
                     + '\n' + 'sd: \t' + str(self.standard_deviation)
                     + '\t\t' + 'cv: \t' + str(self.coefficient_of_variation)
                     + '\t\t' + 'route_to_distance: \t' + str(self.lenth_to_distance) + '\n')
        output.write('raw data: \t')
        for lenth in self.route_lenth:
            output.write(str(lenth) + ' ')
        output.write('\n\n')
        output.close()

        return


class improved_statistics_output(statistics_output):
    def __init__(self, description):
        statistics_output.__init__(self, description)

        self.number_of_turns = list()
        self.average_distance_to_route = list()
        self.maximum_distance_to_route = list()
        self.sum_number_of_turns = 0
        self.sum_average_distance_to_route = 0
        self.sum_maximum_distance_to_route = 0
        self.mean_number_of_turns = 0
        self.mean_average_distance_to_route = 0
        self.mean_maximum_distance_to_route = 0

        return


    def improved_add_one_sample(self, route_lenth, num_of_turns, avrg_dist_to_route, max_dist_to_route):
        statistics_output.add_one_sample(self, route_lenth)

        self.number_of_turns.append(num_of_turns)
        self.average_distance_to_route.append(avrg_dist_to_route)
        self.maximum_distance_to_route.append(max_dist_to_route)
        self.sum_number_of_turns += num_of_turns
        self.sum_average_distance_to_route += avrg_dist_to_route
        self.sum_maximum_distance_to_route += max_dist_to_route

        return


    def improved_calculate_statistics(self):
        statistics_output.calculate_statistics(self)

        self.mean_number_of_turns = self.sum_number_of_turns / self.sample_size
        self.mean_average_distance_to_route = self.sum_average_distance_to_route / self.sample_size
        self.mean_maximum_distance_to_route = self.sum_maximum_distance_to_route / self.sample_size

        return


    def improved_dump_to_file(self, path, flag_clear_old):
        statistics_output.dump_to_file(self, path, flag_clear_old)

        if flag_clear_old is True:
            output = open(path, 'w')
        elif flag_clear_old is False:
            output = open(path, 'a')
        else:
            return

        output.write('number of turns: \t' + str(self.mean_number_of_turns) + '\t\t'
                     + 'average distance to route: \t' + str(self.mean_average_distance_to_route) + '\t\t'
                     + 'max distance to route: \t' + str(self.mean_maximum_distance_to_route) + '\n\n\n')
        output.close()

        return

