#!/usr/bin/python

import numpy as np

def life_step_1(X):
    """Game of life step using generator expressions"""
    nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (nbrs_count == 3) | (np.uint64(X) & (nbrs_count == 2))


import itertools
import pygame
import time
import sys
from pygame.locals import *





def exit_game():
    """

    :return:
    exit the game
    """
    pygame.display.quit()
    sys.exit()


def get_board(size, alive_cons):
    return [[1 if (i, j) in alive_cons else 0
             for j in range(size)]
            for i in range(size)]


def get_neighbors(con):
    x, y = con
    neighbors = [(x + i, y + j)
                 for i in range(-1, 2)
                 for j in range(-1, 2)
                 if not i == j == 0]
    return neighbors


def calculate_alive_neighbors(con, alive_cons):
    # return len(filter(lambda x: x in alive_cons,
    #                   get_neighbors(con)))
    return len([x for x in get_neighbors(con) if x in alive_cons])


def is_alive_con(con, alive_cons):
    alive_neighbors = calculate_alive_neighbors(con, alive_cons)
    if (alive_neighbors == 3 or
            (alive_neighbors == 2 and con in alive_cons)):
        return True
    return False


def new_step(alive_cons):
    board = itertools.chain(*map(get_neighbors, alive_cons))
    new_board = set([con
                     for con in board
                     if is_alive_con(con, alive_cons)])
    return list(new_board)


def is_correct_con(size, con):
    x, y = con
    return all(0 <= coord <= size - 1 for coord in [x, y])


def correct_con(size, con):
    return ((con[0] + size) % size, (con[1] + size) % size)


def correct_cons(size, cons):
    # return filter(lambda x: is_correct_con(size, x), cons)
    cor_cons = list()
    for con in cons:
        if correct_con(size, con) not in cor_cons:
            cor_cons.append(correct_con(size, con))
    # return [x for x in cons if is_correct_con(size, x)]
    return cor_cons


def print_board(board):
    for line in board:
        print(line)
    print


def draw_grid(display_surf, size, width=1):
    """

    :param      display_surf: display surface
    :param      width: width of grid lines

    :return:
    drawing grid on game map
    """
    for y in range(size):
        for x in range(size):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(display_surf, (0, 0, 0), rect, width)


def print_board(surf, board):
    green = (0, 255, 0)
    white = (255, 255, 255)
    l = len(board)
    for y in range(l):
        for x in range(l):
            if board[x][y] == 1:
                color = green
            else:
                color = white
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(surf, color, rect, 0)
            pygame.draw.rect(surf, (0, 0, 0), rect, 1)


def get_active_cell(mouse_pos, size_row, size_col):
    """
    :param      mouse_pos:  mouse position on widow screen

    :return:    cell:   cell... just cell
    """
    for row in range(size_row):
        for column in range(size_col):
            if (column * TILESIZE) <= mouse_pos[0] <= (column * TILESIZE) + TILESIZE:
                if (row * TILESIZE) <= mouse_pos[1] <= (row * TILESIZE) + TILESIZE:
                    cell = (row, column)
                    return cell


def draw_cell(surf, pos, color=(0, 0, 0)):
    rect = pygame.Rect(pos[1] * TILESIZE, pos[0] * TILESIZE, TILESIZE, TILESIZE)
    pygame.draw.rect(surf, color, rect, 0)
    pygame.draw.rect(surf, (0, 0, 0), rect, 1)


def main():
    global STOP
    boards = list()
    pygame.init()
    board = np.zeros((size, size))
    surf = pygame.display.set_mode((size * TILESIZE + 200, size * TILESIZE))

    surf.fill((255, 255, 255))
    draw_grid(surf, size)
    print_board(surf, board)
    draw_cell(surf, (0, size + 1), (255, 0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == MOUSEBUTTONDOWN:
                    # board = correct_cons(size, new_step(board))
                    # print_board(surf, get_board(size, board))
                    # time.sleep(0.5)
                    mouse_pos = pygame.mouse.get_pos()
                    act_cell = get_active_cell(mouse_pos, size, size + 2)
                    print(act_cell)
                    if act_cell == (0, size + 1):
                        STOP = not STOP
                    elif act_cell:
                        draw_cell(surf, act_cell, (0, 255, 0))
                        board[act_cell[1], act_cell[0]] = 1
                    pygame.display.update()
        if not STOP:
            board = life_step_1(board)
            if any((board == x).all() for x in boards):
                STOP = not STOP
            else:
                boards.append(board)

            print_board(surf, board)
            time.sleep(0.1)
        pygame.display.update()


if __name__ == '__main__':
    size = 30
    TILESIZE = int(600 / (size))
    STOP = 1
    main()
