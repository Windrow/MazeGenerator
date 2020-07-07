# Main loop of the process
#pyinstaller -w -F mg_main_application.py mg_function.py mg_definition.py mg_boundary.py

# Imports
from mg_boundary import *
from mg_definition import *
import pygame
from sys import exit
from pygame.locals import *



# Main
pygame.init()
pygame.display.set_caption('Map Generator V2020 Application')

cfg_app = config_application()
management = config_management()
curr_map = None

# Init surface and clock
display_surf = pygame.display.set_mode((cfg_app.display_surf_width_pixel, cfg_app.display_surf_height_pixel),
                                       pygame.FULLSCREEN)
#display_surf = pygame.display.set_mode((cfg_app.display_surf_width_pixel, cfg_app.display_surf_height_pixel))
fps_clock = pygame.time.Clock()

management.init_button_group_list(display_surf)
management.display_buttons()
mouse_up = True

# Main loop
while True:
    for event in pygame.event.get():
        ret = button_ret.NOTHING

        if event.type == QUIT:
            pygame.quit()
            exit()

        elif event.type == MOUSEMOTION:
            if mouse_up is True:
                ret = management.on_mouse_over(event.pos)
            else:
                ret = management.on_pressed(event.pos)
            management.display_update()

        elif event.type == MOUSEBUTTONDOWN:
            ret = management.on_pressed(event.pos)
            mouse_up = False
            if ret != button_ret.NOTHING:
                management.display_update()

        elif event.type == MOUSEBUTTONUP:
            ret = management.on_click(event.pos)
            mouse_up = True
            if ret != button_ret.NOTHING:
                management.display_update()

            if ret == button_ret.GENERATE_MAP:
                # Reinitialize map
                curr_map = []
                print(management.config_list)
                map_shape = management.config_list[config_list_index.MAP_SHAPE]
                curr_map = improved_map_2d_square(map_shape[0][0], map_shape[0][1],
                                                  management.config_list[config_list_index.DISPLAY_GRID_COLOR],
                                                  management.config_list[config_list_index.DISPLAY_GRID_DISTANCE],
                                                  management.config_list[config_list_index.DISPLAY_ROUTE])
                curr_map.improvedGridInit()
                curr_map.initWallLists()
                curr_map.setBorder(d_mask['EMPTY'])
                curr_map.displayClearMap(display_surf)
                pos_x = curr_map.display_pos_set[0] + curr_map.display_pos_set[2] / 2 \
                        - (map_shape[0][1] / 2 + 1) * map_shape[2]
                pos_y = curr_map.display_pos_set[1] + curr_map.display_pos_set[3] / 2 \
                        - (map_shape[0][0] / 2 + 1) * map_shape[2]

                # Entrance and Exit
                if management.config_list[config_list_index.ENTRANCE_EXIT_MODE] == d_entrance_exit_mode['FIXED']:
                    # Fix entrance and exit at top-left corner and bottom-right corner
                    curr_map.improvedSetEntranceAndExitGrid([1, 0], [1, 1],
                                                    [curr_map.row_num, curr_map.column_num + 1],
                                                    [curr_map.row_num, curr_map.column_num])
                elif management.config_list[config_list_index.ENTRANCE_EXIT_MODE] == d_entrance_exit_mode['RANDOM'] \
                        or management.config_list[config_list_index.START_GRID_NUM] == d_start_grid_num['SINGLE']:
                    # Random Entrance and exit
                    curr_map.improvedRandomEntranceAndExitGrid()
                else:
                    # Entrance and exit determined by the connection of the areas
                    pass

                # Get generation starting grid
                curr_map.improvedRandomGenerationStartGrid(management.config_list[config_list_index.START_GRID_NUM])
                curr_map.display_update(display_surf, pos_y, pos_x, map_shape[2])

                # Display map title(map description)
                management.display_map_description()

                pygame.display.update()

            elif ret == button_ret.UPDATE_CONFIG_DISPLAY:
                if curr_map is not None:
                    curr_map.update_display_settings(management.config_list[config_list_index.DISPLAY_GRID_COLOR],
                                                    management.config_list[config_list_index.DISPLAY_GRID_DISTANCE],
                                                    management.config_list[config_list_index.DISPLAY_ROUTE])
                    curr_map.set_all_update_flag(True)
                    if management.config_list[config_list_index.DISPLAY_GRID_COLOR] \
                            == mg_boundary.d_display_grid_color['NO']:
                        management.display_map_statistics((0, 0, 0, 0))
                    else:
                        management.display_map_statistics((curr_map.route.__len__(), curr_map.turns_on_route,
                                                           curr_map.average_distance_to_route, curr_map.max_distance_to_route))
                    curr_map.display_update(display_surf, pos_y, pos_x, map_shape[2])
                    pygame.display.update()

            elif ret == button_ret.EXIT:
                pygame.quit()
                exit()

    if curr_map is not None:
        if curr_map.generation_done is False:
            curr_map.improvedGrowOneRound(management.config_list[config_list_index.GROWTH_RATIO])
            if management.config_list[config_list_index.DISPLAY_GENERATION_PROCESS]:
                curr_map.display_update(display_surf, pos_y, pos_x, map_shape[2])
        elif curr_map.route == list():
            # Connection of the areas
            curr_map.updateWallLists()
            curr_map.updateConnectionMatrix()
            # Find the route
            curr_map.findLongestAreaRoute()
            curr_map.generateLongestAreaRouteEntranceAndExitGrids()
            curr_map.findMultipleStartGridRoute()
            # Calculate and display statistics
            curr_map.calculateTurnsOnRoute()
            curr_map.calculateDistanceToRoute()
            if management.config_list[config_list_index.DISPLAY_GRID_COLOR] == mg_boundary.d_display_grid_color['NO']:
                management.display_map_statistics((0, 0, 0, 0))
            else:
                management.display_map_statistics((curr_map.route.__len__(), curr_map.turns_on_route,
                                                   curr_map.average_distance_to_route, curr_map.max_distance_to_route))

            curr_map.set_all_update_flag(True)
            curr_map.display_update(display_surf, pos_y, pos_x, map_shape[2])

    pygame.display.update()

    fps_clock.tick(cfg_app.fps)

