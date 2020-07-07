# Functions defined here

# Imports
import pygame
from random import random


# Functions
# Random sampling n out of m
def randomSampling(m, n):
    index_list = list()
    j = 0

    if m != 0:
        for i in range(m):
            if random() < (n - j) / (m - i):
                index_list.append(i)
                j += 1
            if j == n:
                break

    return index_list


# A sequence mixing up n elements
def randomSequence(n):
    index_list = list()
    rand_list = list()
    equal_flag = 0

    if n != 0:
        while True:
            for i in range(n):
                rand_list.append(random())
            for i in range(n):
                count = 0
                for j in range(n):
                    if rand_list[j] == rand_list[i] and i != j:
                        equal_flag = 1
                        break
                    if rand_list[j] < rand_list[i]:
                        count += 1
                if equal_flag == 1:
                    break
                index_list.append(count)
            if equal_flag == 0:
                break

    return index_list


# Used by findLargestRouteWithoutOverlap
def findLargestRouteTraversalOneMoreNode(curr_list, option_table, index_list):
    global work_count
    work_count += 1

    for area in option_table[curr_list[-1]]:
        if area not in curr_list:
            curr_list.append(area)
            index_list = findLargestRouteTraversalOneMoreNode(curr_list, option_table, index_list)
            curr_list.pop()
        if area == 0:
            curr_list.append(area)
            if curr_list.__len__() > index_list.__len__():
                index_list = curr_list.copy()
            curr_list.pop()

    return index_list


# Find a route containing the most check points out of n, input (n + 1) * (n + 1) table
# First row indicate connection to border
# Return an area index sequence including from and to border at two ends
def findLargestRouteWithoutOverlap(connection_matrix):
    curr_list = [0]
    index_list = curr_list.copy()
    n = connection_matrix.__len__() - 1

    option_table = [list() for i in range(n + 1)]
    for i in range(n + 1):
        for j in range(n + 1):
            if connection_matrix[i][j] != 0:
                option_table[i].append(j)

    global work_count
    work_count = 0

    return findLargestRouteTraversalOneMoreNode(curr_list, option_table, index_list)


# Used by findLongestRouteWithoutOverlap
def findLongestRouteTraversalOneMoreNode(curr_list, curr_length, distance_matrix, option_table, index_list):
    global work_count
    work_count += 1
    global length

    for area in option_table[curr_list[-1]]:
        if area not in curr_list:
            curr_list.append(area)
            index_list = findLongestRouteTraversalOneMoreNode(curr_list, curr_length + distance_matrix[curr_list[-2]][area],
                                                              distance_matrix, option_table, index_list)
            curr_list.pop()
        if area == 0:
            curr_list.append(area)
            if curr_length + distance_matrix[curr_list[-1]][area] > length:
                index_list = curr_list.copy()
                length = curr_length + distance_matrix[curr_list[-2]][area]
            curr_list.pop()

    return index_list


# Find a route with the largest sum distance, input (n + 1) * (n + 1) table
# -1 for no connection
def findLongestRouteWithoutOverlap(distance_matrix):
    curr_list = [0]
    curr_length = 0
    index_list = curr_list.copy()
    global length
    length = 0
    n = distance_matrix.__len__() - 1

    option_table = [list() for i in range(n + 1)]
    for i in range(n + 1):
        for j in range(n + 1):
            if distance_matrix[i][j] != -1:
                option_table[i].append(j)

    global work_count
    work_count = 0

    return findLongestRouteTraversalOneMoreNode(curr_list, curr_length, distance_matrix, option_table, index_list)


# 0 - 255 for RGB value
def colorValidation(color):
    for i in range(3):
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
            color[i] = 0

    return color


# Display a text, why it is so costly.
def textDisplay(string, font, size, color, center_x, center_y):
    text_font = pygame.font.SysFont(font, size)
    text_surf = text_font.render(string, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = (center_x, center_y)

    return text_surf, text_rect


def textDisplayTopLeftAligned(string, font, size, color, pos_x, pos_y):
    text_font = pygame.font.SysFont(font, size)
    text_surf = text_font.render(string, True, color)
    text_rect = text_surf.get_rect()
    text_rect.center = (pos_x + text_rect.w / 2, pos_y + text_rect.h / 2)

    return text_surf, text_rect


def getDictionaryKeyWithValue(dictionary, value):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

