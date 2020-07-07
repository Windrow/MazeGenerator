from mg_boundary import *
from mg_definition import *
import pygame, sys
from pygame.locals import *


input_variables = list()
'''
input_variables.append(['16*16 fixed-e2e single-start-grid ratio=0.2',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['NORMAL']])

input_variables.append(['16*16 fixed-e2e single-start-grid ratio=0.05',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['LOW']])

input_variables.append(['16*16 fixed-e2e single-start-grid ratio=0.4',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['HIGH']])

input_variables.append(['16*16 fixed-e2e single-start-grid ratio=1',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['ONE']])

input_variables.append(['16*16 fixed-e2e 8-start-grid ratio=0.2',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SOME'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['NORMAL']])

input_variables.append(['16*16 fixed-e2e 8-start-grid ratio=0.05',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SOME'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['LOW']])

input_variables.append(['16*16 fixed-e2e 8-start-grid ratio=0.4',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SOME'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['HIGH']])

input_variables.append(['16*16 fixed-e2e 8-start-grid ratio=1',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SOME'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['ONE']])

input_variables.append(['16*16 fixed-e2e 4-start-grid ratio=0.2',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['FEW'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['NORMAL']])

input_variables.append(['16*16 fixed-e2e 8-start-grid ratio=0.2',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SOME'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['NORMAL']])

input_variables.append(['16*16 fixed-e2e 16-start-grid ratio=0.2',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['MANY'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['NORMAL']])

input_variables.append(['16*16 random-e2e 8-start-grid ratio=0.2',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SOME'],
                        d_entrance_exit_mode['RANDOM'],
                        d_growth_ratio['NORMAL']])

input_variables.append(['16*16 derived-e2e 8-start-grid ratio=0.2',
                        d_map_shape['SQ_NORMAL'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SOME'],
                        d_entrance_exit_mode['DERIVED'],
                        d_growth_ratio['NORMAL']])
'''
input_variables.append(['32*32 fixed-e2e single-start-grid ratio=0.2',
                        d_map_shape['SQ_LARGE'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['NORMAL']])

input_variables.append(['32*32 fixed-e2e single-start-grid ratio=0.05',
                        d_map_shape['SQ_LARGE'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['LOW']])

input_variables.append(['32*32 fixed-e2e single-start-grid ratio=0.4',
                        d_map_shape['SQ_LARGE'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['HIGH']])

input_variables.append(['32*32 fixed-e2e single-start-grid ratio=1',
                        d_map_shape['SQ_LARGE'],
                        d_start_grid_mode['RANDOM'],
                        d_start_grid_num['SINGLE'],
                        d_entrance_exit_mode['FIXED'],
                        d_growth_ratio['ONE']])


pygame.init()
pygame.display.set_caption('Map Generator V2020 Improved Statistics')
display_surf = pygame.display.set_mode((mg_boundary.display_surf_width_pixel, mg_boundary.display_surf_height_pixel))
fps_clock = pygame.time.Clock()

for curr_condition in input_variables:
    curr_output = improved_statistics_output(curr_condition[0])

    for sample_num in range(sampling_size):
        curr_map = improved_map_2d_square(curr_condition[1][0][0], curr_condition[1][0][1],
                                          d_display_grid_color['NO'],
                                          d_display_grid_distance['OFF'],
                                          d_display_route['OFF'])

        curr_map.improvedGridInit()
        curr_map.initWallLists()
        curr_map.setBorder(d_mask['EMPTY'])
        curr_map.displayClearMap(display_surf)

        if curr_condition[4] == d_entrance_exit_mode['FIXED']:
            # Fix entrance and exit at top-left corner and bottom-right corner
            curr_map.improvedSetEntranceAndExitGrid([1, 0], [1, 1],
                                                    [curr_map.row_num, curr_map.column_num + 1],
                                                    [curr_map.row_num, curr_map.column_num])
        elif curr_condition[4] == d_entrance_exit_mode['RANDOM'] or curr_condition[3] == d_start_grid_num['SINGLE']:
            # Random Entrance and exit
            curr_map.improvedRandomEntranceAndExitGrid()
        else:
            # Entrance and exit determined by the connection of the areas
            pass

        # Get generation starting grid
        curr_map.improvedRandomGenerationStartGrid(curr_condition[3])
        curr_map.display_update(display_surf, 0, 0, curr_condition[1][2])

        while curr_map.generation_done is False:
            # Events handlers
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Generation round
            curr_map.improvedGrowOneRound(curr_condition[5])
            fps_clock.tick(fps)

        # Connection of the areas
        curr_map.updateWallLists()
        curr_map.updateConnectionMatrix()
        # Find the route
        curr_map.findLongestAreaRoute()
        curr_map.generateLongestAreaRouteEntranceAndExitGrids()
        #curr_map.findLargestAreaRoute()
        #curr_map.generateRandomEntranceAndExitGrids()
        curr_map.findMultipleStartGridRoute()
        # Calculate and display statistics
        curr_map.calculateTurnsOnRoute()
        curr_map.calculateDistanceToRoute()

        curr_output.improved_add_one_sample(curr_map.route.__len__(), curr_map.turns_on_route,
                                            curr_map.average_distance_to_route, curr_map.max_distance_to_route)

        curr_map.set_all_update_flag(True)
        curr_map.display_update(display_surf, 0, 0, curr_condition[1][2])
        pygame.display.update()

    curr_output.update_e2e_distance(curr_condition[1][0][0] + curr_condition[1][0][1] - 1)
    curr_output.improved_calculate_statistics()
    curr_output.improved_dump_to_file(output_file_path, False)

