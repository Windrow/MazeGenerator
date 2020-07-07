# Main loop of the process

# Imports
from mg_boundary import *
from mg_definition import *
import pygame, sys
from pygame.locals import *


# Variables
# Entrance and exit, 1 for fixed, 0 for random, -1 for generated
fix_entrance_and_exit = 1

input_variables = list()

input_variables.append(
        boundary_condition_struct('16*16 empty-mask 4-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['NORMAL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_NORMAL'][0], d_map_size['SQ_NORMAL'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['FEW'],
                                  d_growth_ratio['NORMAL']))
'''
input_variables.append(
        boundary_condition_struct('16*16 empty-mask 8-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['NORMAL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_NORMAL'][0], d_map_size['SQ_NORMAL'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['SOME'],
                                  d_growth_ratio['NORMAL']))

input_variables.append(
        boundary_condition_struct('32*32 empty-mask 32-start-grid ratio=0.2',
                                  d_fps['HIGH'],
                                  d_display_surf_size_pixel['HD'][0], d_display_surf_size_pixel['HD'][1],
                                  d_grid_size_pixel['SMALL'],
                                  d_wall_thickness_pixel['NORMAL'],
                                  d_map_size['SQ_LARGE'][0], d_map_size['SQ_LARGE'][1],
                                  d_mask['EMPTY'],
                                  d_start_grid_num['DANGEROUS'],
                                  d_growth_ratio['NORMAL']))
'''

# Main
pygame.init()
pygame.display.set_caption('Map Generator V2020 Improved')

for i in range(input_variables.__len__()):
    curr_condition = input_variables[i]
    curr_output = statistics_output(curr_condition.description)

    # Init surface and clock
    display_surf = pygame.display.set_mode((curr_condition.display_surf_width_pixel,
                                            curr_condition.display_surf_height_pixel))
    fps_clock = pygame.time.Clock()

    for sample_num in range(sampling_size):
        # Init map
        curr_map = improved_map_2d_square(curr_condition.row_num, curr_condition.column_num, 1, 1, 1)
        curr_map.improvedGridInit()
        curr_map.setBorder(curr_condition.mask)
        curr_map.displayClearAll(display_surf)
        curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        pygame.display.update()
        print('MS 1')

        # Entrance and Exit
        if fix_entrance_and_exit == 1:
            # Fix entrance and exit at top-left corner and bottom-right corner
            curr_map.improvedSetEntranceAndExitGrid([1, 0], [1, 1],
                                            [curr_map.row_num, curr_map.column_num + 1],
                                            [curr_map.row_num, curr_map.column_num])
        elif fix_entrance_and_exit == 0:
            # Random Entrance and exit
            curr_map.improvedRandomEntranceAndExitGrid()
        # else
            # Entrance and exit determined by the connection of the areas
        print('MS 2')

        # Get generation starting grid
        curr_map.improvedRandomGenerationStartGrid(curr_condition.start_grid_num)
        curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        pygame.display.update()
        print('MS 3')

        # Generation loop
        while curr_map.generation_done is False:
            # Events handlers
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Generation round
            curr_map.improvedGrowOneRound(curr_condition.growth_ratio)
            #curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
            #pygame.display.update()
            fps_clock.tick(curr_condition.fps)
        print('MS 4')

        # Connection of the areas
        curr_map.initWallLists()
        curr_map.updateConnectionMatrix()
        curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        pygame.display.update()
        print('MS 5')

        # Find the route
        #curr_map.findLargestAreaRoute()
        #curr_map.generateRandomEntranceAndExitGrids()
        curr_map.findLongestAreaRoute()
        curr_map.generateLongestAreaRouteEntranceAndExitGrids()

        curr_map.findMultipleStartGridRoute()
        curr_map.display(display_surf, 0, 0, curr_condition.grid_size_pixel)
        pygame.display.update()
        print('MS 6')

        # Statistics
        curr_map.calculateDistanceToRoute()
        curr_output.add_one_sample(curr_map.route.__len__())
        curr_map.displayWallOnly(display_surf, 0, curr_condition.display_surf_width_pixel / 2,
                                 curr_condition.grid_size_pixel)
        pygame.display.update()
        print('MS 7')

        break_flag = 1
        while break_flag == 0:
            # Events handlers
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    break_flag = 1

    # For current fixed entrance and exit
    curr_output.update_e2e_distance(curr_condition.row_num + curr_condition.column_num - 1)
    # Save the result to file
    curr_output.calculate_statistics()
    curr_output.dump_to_file(output_file_path, False)

pygame.quit()
sys.exit()