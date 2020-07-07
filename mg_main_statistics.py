# Main loop of the process

# Imports
from mg_boundary import *
from mg_definition import *
import pygame, sys
from pygame.locals import *


# Variables
input_variables = list()
'''
input_variables.append(
        boundary_condition_struct('8*8 empty-mask single-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['LARGE'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_SMALL'][0], d_map_size['SQ_SMALL'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['NORMAL']))

input_variables.append(
        boundary_condition_struct('16*16 empty-mask single-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['NORMAL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_NORMAL'][0], d_map_size['SQ_NORMAL'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['NORMAL']))

input_variables.append(
        boundary_condition_struct('32*32 empty-mask single-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['SMALL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_LARGE'][0], d_map_size['SQ_LARGE'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['NORMAL']))

input_variables.append(
        boundary_condition_struct('16*16 empty-mask single-start-grid ratio=0.05',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['NORMAL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_NORMAL'][0], d_map_size['SQ_NORMAL'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['LOW']))

input_variables.append(
        boundary_condition_struct('16*16 empty-mask single-start-grid ratio=0.4',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['NORMAL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_NORMAL'][0], d_map_size['SQ_NORMAL'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['HIGH']))

input_variables.append(
        boundary_condition_struct('16*32 empty-mask single-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['NORMAL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['RECT_NORMAL'][0], d_map_size['RECT_NORMAL'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['NORMAL']))

input_variables.append(
        boundary_condition_struct('32*64 empty-mask single-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['SMALL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['RECT_LARGE'][0], d_map_size['RECT_LARGE'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['NORMAL']))
'''
input_variables.append(
        boundary_condition_struct('32*64 cutting-mask single-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['SMALL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['RECT_LARGE'][0], d_map_size['RECT_LARGE'][1],
                                  d_mask['CUT_MORE'],
                                  d_start_grid_num['SINGLE'],
                                  d_growth_ratio['NORMAL']))

# Main
pygame.init()
pygame.display.set_caption('Map Generator V2020 Statistics')

for curr_condition in input_variables:
    curr_output = statistics_output(curr_condition.description)

    # Init surface and clock
    display_surf = pygame.display.set_mode((curr_condition.display_surf_width_pixel,
                                            curr_condition.display_surf_height_pixel))
    fps_clock = pygame.time.Clock()

    for sample_num in range(sampling_size):
        # Init map
        curr_map = basic_map_2d_square(curr_condition.row_num, curr_condition.column_num)
        curr_map.gridInit()
        curr_map.setBorder(curr_condition.mask)
        curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        #pygame.display.update()

        # Fix entrance and exit at top-left corner and bottom-right corner
        curr_map.setEntranceAndExitGrid([1, 0], [1, 1],
                                        [curr_map.row_num, curr_map.column_num + 1],
                                        [curr_map.row_num, curr_map.column_num])
        #curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        #pygame.display.update()

        # Get generation starting grid
        curr_map.randomGenerationStartGrid(curr_condition.start_grid_num)
        #curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        #pygame.display.update()

        # Generation loop
        while curr_map.generation_done is False:
            # Events handlers
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Generation round
            curr_map.growOneRound(curr_condition.growth_ratio)
            #curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
            #pygame.display.update()
            fps_clock.tick(curr_condition.fps)
        curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        pygame.display.update()

        # Find the route
        curr_map.findSingleStartGridRoute()
        curr_output.add_one_sample(curr_map.route.__len__())
        curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        pygame.display.update()

    # For current fixed entrance and exit
    curr_output.update_e2e_distance(curr_condition.row_num + curr_condition.column_num - 1)
    # Save the result to file
    curr_output.calculate_statistics()
    curr_output.dump_to_file(output_file_path, False)

