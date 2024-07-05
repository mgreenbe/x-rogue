from constants import *
from monster import *
from random import randint
import random
import numpy as np
import pandas as pd
import hero

rng = np.random.default_rng()
counter = 0
map = np.full((ROWS - 1, COLS), SPACE, dtype=np.int8)
room_matrix = np.full_like(map, fill_value=-1)
rooms = []
visited_rooms = set()
monsters = pd.DataFrame()


def make_room(i, j):
    v_padding = rng.integers(
        0, GRID_ROW_HEIGHT - 2 - MIN_ROOM_HEIGHT, endpoint=True, dtype=int
    )
    h_padding = rng.integers(
        0, GRID_COL_WIDTH - 2 - MIN_ROOM_WIDTH, endpoint=True, dtype=int
    )
    h = GRID_ROW_HEIGHT - v_padding
    w = GRID_COL_WIDTH - h_padding
    top_padding = rng.integers(0, v_padding, endpoint=True, dtype=int)
    left_padding = rng.integers(0, h_padding, endpoint=True, dtype=int)
    y = i * GRID_ROW_HEIGHT + i + top_padding
    x = j * GRID_COL_WIDTH + j + left_padding
    return y, x, h, w


def draw_rooms():
    for y, x, h, w in rooms:
        map[y, x : x + w] = DASH
        map[y + h - 1, x : x + w] = DASH
        map[y + 1 : y + h - 1, x] = PIPE
        map[y + 1 : y + h - 1, x + w - 1] = PIPE
        map[y + 1 : y + h - 1, x + 1 : x + w - 1] = DOT


def draw_horiz_passage(i, j):
    assert i < j
    assert i // GRID_COLS == j // GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, hj, _] = rooms[j]
    yi = yi + randint(1, hi - 2)
    yj = yj + randint(1, hj - 2)
    map[yi, xi + wi - 1] = PLUS
    map[yj, xj] = PLUS
    draw_passage(yi, xi + wi, yj, xj - 1)


def draw_vert_passage(i, j):
    assert i < j
    assert i % GRID_COLS == j % GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, _, wj] = rooms[j]
    xi = xi + randint(1, wi - 2)
    xj = xj + randint(1, wj - 2)
    map[yi + hi - 1, xi] = PLUS
    map[yj, xj] = PLUS

    if xi <= xj:
        draw_passage(yi + hi, xi, yj - 1, xj)
    else:
        draw_passage(yj - 1, xj, yi + hi, xi)


def draw_passage(y0, x0, y1, x1):
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


def init(rng_=None):
    global rng
    global counter
    global map
    global room_matrix
    global rooms
    global visited_rooms
    global monsters

    if rng_ is not None:
        rng = rng_
    counter = 0
    map = np.full((ROWS - 1, COLS), SPACE, dtype=np.int8)
    rooms = [make_room(i, j) for i in range(GRID_ROWS) for j in range(GRID_COLS)]
    for i, [y, x, h, w] in enumerate(rooms):
        room_matrix[y : y + h, x : x + w] = i
    visited_rooms = set()
    draw_rooms()
    for i, j in [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8)]:
        draw_horiz_passage(i, j)
    for i, j in [(0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8)]:
        draw_vert_passage(i, j)
    monsters_list = []
    for i, (y, x, h, w) in enumerate(rooms):
        monster_type = random.choice(monster_types)
        hp = monster_type["level"] * randint(1, 8)
        monster: Monster = dict(
            **monster_type,
            id=counter,
            hp=hp,
            max_hp=hp,
            y=y + randint(1, h - 2),
            x=x + randint(1, w - 2),
            curroom=i,
            status="idle"
        )
        counter += 1
        monsters_list.append(monster)
        monsters = pd.DataFrame(monsters_list)

    # Put the hero in a random spot in a random room.
    # Make sure there's no monster there.
    while True:
        [y, x, h, w] = random.choice(rooms)
        hero.y = randint(y + 1, y + h - 2)
        hero.x = randint(x + 1, x + w - 2)
        if all(np.logical_or(monsters.y != hero.y, monsters.x != hero.x)):
            hero.curroom = room_matrix[hero.y, hero.x]
            visited_rooms.add(hero.curroom)
            break
