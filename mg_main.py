# Main loop of the process

# Imports
import mg_boundary, mg_definition
import pygame, sys
from pygame.locals import *



# Variables
FPS = 2



# Main
pygame.init()
display_surf = pygame.display.set_mode((mg_boundary.display_surf_width_pixel, mg_boundary.display_surf_height_pixel))
pygame.display.set_caption('Map Generator V2020')
fps_clock = pygame.time.Clock()

map = mg_definition.basic_map_2d_square(mg_boundary.row_num, mg_boundary.column_num)
map.gridInit()

map.setBorder(mg_boundary.mask)
map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
pygame.display.update()

#map.randomEntranceAndExitGrid()
map.setEntranceAndExitGrid([1, 0], [1, 1], [map.row_num, map.column_num + 1], [map.row_num, map.column_num])
map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
pygame.display.update()

map.randomGenerationStartGrid(mg_boundary.start_grid_num)
map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
pygame.display.update()

i = 0

while map.generation_done is False:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #map.growOneRound(mg_boundary.growth_ratio)
    #map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
    #pygame.display.update()

    if i % 3 == 0:
        map.growFromNewbornToGrowing()
        map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
        pygame.display.update()
    elif i % 3 == 1:
        map.growFromMatureToGraven()
        map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
        pygame.display.update()
    elif i % 3 == 2:
        map.growFromGrowingToMature(mg_boundary.growth_ratio)
        map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
        pygame.display.update()
        map.isGrenerationDone()
    i += 1

    fps_clock.tick(FPS)

#map.calculateDistance(map.start_grid[0].pos_x, map.start_grid[0].pos_y)
map.findSingleStartGridRoute()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    map.display(display_surf, 32, 32, mg_boundary.grid_size_pixel)
    pygame.display.update()
    fps_clock.tick(FPS)


