#!/usr/bin/python

import itertools
import pygame
import time
import sys
from pygame.locals import *


size = 20
TILESIZE = int(600/(size))


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
            #draw_grid(surf, l)


def main():
    pygame.init()
    board = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3), (4, 3), (1, 1), (2, 2), (5, 1)]
    surf = pygame.display.set_mode((size * TILESIZE, size * TILESIZE))
    surf.fill((255, 255, 255))
    draw_grid(surf, size)
    print_board(surf, get_board(size, board))
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == MOUSEBUTTONDOWN:
                    # board = correct_cons(size, new_step(board))
                    # print_board(surf, get_board(size, board))
                    # time.sleep(0.5)
                    pygame.display.update()
        board = correct_cons(size, new_step(board))
        print_board(surf, get_board(size, board))
        time.sleep(0.2)
        pygame.display.update()


if __name__ == '__main__':
    main()
