from constants import *
from monster import *
from random import randint
import random
import numpy as np
import pandas as pd


def make_room(i, j):
    v_padding = randint(0, GRID_ROW_HEIGHT - 2 - MIN_ROOM_HEIGHT)
    h_padding = randint(0, GRID_COL_WIDTH - 2 - MIN_ROOM_WIDTH)
    h = GRID_ROW_HEIGHT - v_padding
    w = GRID_COL_WIDTH - h_padding
    top_padding = randint(0, v_padding)
    left_padding = randint(0, h_padding)
    y = i * GRID_ROW_HEIGHT + i + top_padding
    x = j * GRID_COL_WIDTH + j + left_padding
    return y, x, h, w


def draw_rooms(rooms, map):
    for y, x, h, w in rooms:
        map[y, x : x + w] = DASH
        map[y + h - 1, x : x + w] = DASH
        map[y + 1 : y + h - 1, x] = PIPE
        map[y + 1 : y + h - 1, x + w - 1] = PIPE
        map[y + 1 : y + h - 1, x + 1 : x + w - 1] = DOT


def draw_horiz_passage(i, j, rooms, map):
    assert i < j
    assert i // GRID_COLS == j // GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, hj, _] = rooms[j]
    yi = yi + randint(1, hi - 2)
    yj = yj + randint(1, hj - 2)
    map[yi, xi + wi - 1] = PLUS
    map[yj, xj] = PLUS
    draw_passage(yi, xi + wi, yj, xj - 1, map)


def draw_vert_passage(i, j, rooms, map):
    assert i < j
    assert i % GRID_COLS == j % GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, _, wj] = rooms[j]
    xi = xi + randint(1, wi - 2)
    xj = xj + randint(1, wj - 2)
    map[yi + hi - 1, xi] = PLUS
    map[yj, xj] = PLUS

    if xi <= xj:
        draw_passage(yi + hi, xi, yj - 1, xj, map)
    else:
        draw_passage(yj - 1, xj, yi + hi, xi, map)


def draw_passage(y0, x0, y1, x1, map):
    ymin = min(y0, y1)
    ymax = max(y0, y1)
    ys = [randint(ymin, ymax) for _ in range(abs(x1 - x0))]
    ys.sort()
    ys.append(ymax)
    s, x = (1, x0) if y0 <= y1 else (-1, x1)
    yprev = ymin
    for y in ys:
        map[yprev : y + 1, x] = HASH
        yprev = y
        x += s


counter = 0


def make_level():
    global counter
    map = np.full(
        (ROWS - 1, COLS), SPACE, dtype=np.int8
    )  # stealing name of a built-in function
    rooms = [make_room(i, j) for i in range(GRID_ROWS) for j in range(GRID_COLS)]
    draw_rooms(rooms, map)
    for i, j in [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8)]:
        draw_horiz_passage(i, j, rooms, map)
    for i, j in [(0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8)]:
        draw_vert_passage(i, j, rooms, map)

    monsters = []
    for y, x, h, w in rooms:
        monster_type = random.choice(monster_types)
        hp = monster_type["level"] * randint(1, 8)
        pos = (y + randint(1, h - 2), x + randint(1, w - 2))
        monster: Monster = dict(**monster_type, id=counter, hp=hp, max_hp=hp, pos=pos)
        counter += 1
        monsters.append(monster)
    return rooms, map, pd.DataFrame(monsters)
