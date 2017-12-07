#!/usr/bin/python

import os
import numpy as np
import itertools
import pygame
import time
import sys
from pygame.locals import *


def life_step_1(X):
    """Game of life step using generator expressions"""
    nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (nbrs_count == 3) | (np.uint64(X) & (nbrs_count == 2))


def exit_game():
    """

    :return:
    exit the game
    """
    pygame.display.quit()
    sys.exit()


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


def print_board(surf, board, grid=True, cell_color=(0, 255, 0)):
    white = (255, 255, 255)
    l = len(board)
    for y in range(l):
        for x in range(l):
            if board[x][y] == 1:
                color = cell_color
            else:
                color = white
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(surf, color, rect, 0)
            if grid:
                pygame.draw.rect(surf, (240, 240, 240), rect, 1)


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


def in_button(mouse_pos, button_pos, button_size):
    if (button_pos[0] * BLOCK_SIZE) <= mouse_pos[0] <= (button_pos[0] * BLOCK_SIZE) + BLOCK_SIZE * button_size[0]:
        if (button_pos[1] * TILESIZE) <= mouse_pos[1] <= (button_pos[1] * TILESIZE) + BLOCK_SIZE * button_size[1]:
            return True
    return False


def draw_cell(surf, pos, color=(0, 0, 0), grid=True):
    rect = pygame.Rect(pos[1] * TILESIZE, pos[0] * TILESIZE, TILESIZE, TILESIZE)
    pygame.draw.rect(surf, color, rect, 0)
    if grid:
        pygame.draw.rect(surf, (0, 0, 0), rect, 1)


def main():
    gen_number = 0
    some_color = (100, 100, 100)
    white = (255, 255, 255)
    light_grey = (128, 128, 128)
    yellow = (255, 255, 0)
    green = (0, 255, 0)
    global STOP
    global END_GAME
    boards = list()
    pygame.init()
    board = np.zeros((size, size))
    surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Игра "Жизнь"')
    surf.fill((255, 255, 255))
    print_board(surf, board, BORDER)
    draw_button(surf, START_BUTTON_POS, START_BUTTON_SIZE, some_color)
    pos = START_BUTTON_POS
    but_size = START_BUTTON_SIZE
    draw_msg(surf, 'Старт', ((pos[0] + but_size[0] / 4) * BLOCK_SIZE, (pos[1]) * TILESIZE), BUTTON_TEXT_SIZE, white)
    draw_button(surf, SHUFFLE_BUTTON_POS, SHUFFLE_BUTTON_SIZE, some_color)
    pos = SHUFFLE_BUTTON_POS
    but_size = SHUFFLE_BUTTON_SIZE
    draw_msg(surf, 'Рандом', ((pos[0] + but_size[0] / 4) * BLOCK_SIZE, (pos[1]) * TILESIZE), BUTTON_TEXT_SIZE, white)
    draw_button(surf, CLEAR_BUTTON_POS, CLEAR_BUTTON_SIZE, some_color)
    pos = CLEAR_BUTTON_POS
    but_size = CLEAR_BUTTON_SIZE
    draw_msg(surf, 'Очистить', ((pos[0] + but_size[0] / 6) * BLOCK_SIZE, (pos[1]) * TILESIZE), BUTTON_TEXT_SIZE, white)
    print_board(surf, board, BORDER, green)
    draw_msg(surf, 'Номер поколения: ', (size * TILESIZE + 10, SCREEN_HEIGHT / 3), bold=False)
    draw_msg(surf, gen_number.__str__(), (size * TILESIZE + 140, SCREEN_HEIGHT / 3), bold=False)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    act_cell = get_active_cell(mouse_pos, size, size)
                    print(act_cell)
                    if in_button(mouse_pos, START_BUTTON_POS, START_BUTTON_SIZE):
                        STOP = not STOP
                    if in_button(mouse_pos, SHUFFLE_BUTTON_POS, SHUFFLE_BUTTON_SIZE):
                        if END_GAME:
                            draw_msg(
                                surf,
                                '',
                                (size * TILESIZE / 3, size * TILESIZE / 2.5),
                                erase=True,
                            )
                        print('shuffle')
                        STOP = 1
                        board = np.random.randint(0, 2, (size, size))
                        print_board(surf, board, BORDER, green)
                        gen_number = 0
                        draw_msg(surf, gen_number.__str__(), (size * TILESIZE + 140, SCREEN_HEIGHT / 3), erase=True)
                        END_GAME = 0
                    if in_button(mouse_pos, CLEAR_BUTTON_POS, CLEAR_BUTTON_SIZE):
                        if END_GAME:
                            draw_msg(
                                surf,
                                '',
                                (size * TILESIZE / 3, size * TILESIZE / 2.5),
                                erase=True,
                            )
                        STOP = 1
                        board = np.zeros((size, size))
                        print_board(surf, board, BORDER, green)
                        gen_number = 0
                        draw_msg(surf, gen_number.__str__(), (size * TILESIZE + 140, SCREEN_HEIGHT / 3), erase=True)
                        END_GAME = 0
                    elif act_cell:
                        draw_cell(surf, act_cell, green, False)
                        board[act_cell[1], act_cell[0]] = 1
                    # pygame.display.update()
            elif event.type == MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    act_cell = get_active_cell(mouse_pos, size, size)
                    if act_cell:
                        draw_cell(surf, act_cell, green, False)
                        board[act_cell[1], act_cell[0]] = 1

        if not STOP:
            board = life_step_1(board)
            if any((board == x).all() for x in boards):
                STOP = not STOP
                print('end game')
                draw_msg(
                    surf,
                    'Конец Игры',
                    (size * TILESIZE / 3, size * TILESIZE / 2.5),
                    fontsize=30,
                    bold=True,
                    erase=False,
                    color=pygame.Color('red')
                )
                END_GAME = 1
                del boards
                boards = list()
            else:
                if len(boards) > 1024:
                    del boards[0]
                boards.append(board)
            gen_number += 1
            if not END_GAME:
                print_board(surf, board, BORDER, green)
                draw_msg(surf, gen_number.__str__(), (size * TILESIZE + 140, SCREEN_HEIGHT / 3), erase=True)
            time.sleep(0.1)
        pygame.display.update()


def draw_msg(surf, text, pos, fontsize=13, color=(0, 0, 0), bold=True, erase=False):
    myfont = pygame.font.SysFont("monospace", fontsize, bold)
    if erase:
        surf.fill(pygame.Color("white"), (pos[0], pos[1], SCREEN_WIDTH, pos[1] + len(text) * fontsize))
    label = myfont.render(text, 1, color)
    surf.blit(label, pos)


def draw_button(surf, pos, button_size, color, text=''):
    rect = pygame.Rect(pos[0] * BLOCK_SIZE, pos[1] * TILESIZE, BLOCK_SIZE * button_size[0], BLOCK_SIZE * button_size[1])
    pygame.draw.rect(surf, color, rect, 0)
    pygame.draw.rect(surf, (0, 0, 0), rect, 1)
    ...


if __name__ == '__main__':
    size = 10
    if size > 100:
        BORDER = 0
    else:
        BORDER = 1
    END_GAME = 0
    BLOCK_SIZE = 20
    BUTTON_TEXT_SIZE = 30
    TILESIZE = 630 / size

    SCREEN_WIDTH = round(size * TILESIZE + 200)
    SCREEN_HEIGHT = round(size * TILESIZE + BLOCK_SIZE * 2)
    STOP = 1
    wid = size * TILESIZE / (3 * BLOCK_SIZE)
    START_BUTTON_POS = (0, size)
    SHUFFLE_BUTTON_POS = (wid, size)
    CLEAR_BUTTON_POS = (2 * wid, size)
    START_BUTTON_SIZE = (wid, 2)
    SHUFFLE_BUTTON_SIZE = (wid, 2)
    CLEAR_BUTTON_SIZE = (wid, 2)
    # os.environ['SDL_VIDEO_CENTERED'] = '1'
    pos_wnd_x = round((1366 - SCREEN_WIDTH) / 2)
    os.environ['SDL_VIDEO_WINDOW_POS'] = pos_wnd_x.__str__()+',30'
    main()
