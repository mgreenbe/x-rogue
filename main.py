from random import randint, seed
from zmq.log.handlers import PUBHandler
import numpy as np
import curses
import logging
import time

zmq_log_handler = PUBHandler("tcp://127.0.0.1:12345")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(zmq_log_handler)
time.sleep(0.5)
logger.info(f"x-rogue started, log level {logger.level}")

ROWS = 24
COLS = 80
GRID_ROWS = 3
GRID_COLS = 3
GRID_ROW_HEIGHT = 7
GRID_COL_WIDTH = 26
MIN_ROOM_HEIGHT = 2
MINROOMWIDTH = 2

# seed(0)


def make_room(i, j):
    v_padding = randint(0, GRID_ROW_HEIGHT - 2 - MIN_ROOM_HEIGHT)
    h_padding = randint(0, GRID_COL_WIDTH - 2 - MINROOMWIDTH)

    h = GRID_ROW_HEIGHT - v_padding - 1
    w = GRID_COL_WIDTH - h_padding

    top_padding = randint(0, v_padding)
    left_padding = randint(0, h_padding)

    y = i * GRID_ROW_HEIGHT + i + top_padding
    x = j * GRID_COL_WIDTH + j + left_padding

    return y, x, h, w


def make_rooms():
    rooms = []
    for i in range(GRID_ROWS):
        for j in range(GRID_COLS):
            room = make_room(i, j)
            rooms.append(room)
    return rooms


def draw_room(map):
    for y, x, h, w in rooms:
        map[y, x : x + w] = ord("-")
        map[y + h - 1, x : x + w] = ord("-")
        map[y + 1 : y + h - 1, x] = ord("|")
        map[y + 1 : y + h - 1, x + w - 1] = ord("|")
        map[y + 1 : y + h - 1, x + 1 : x + w - 1] = ord(".")


map = np.full(
    (ROWS - 1, COLS), ord(" "), dtype=np.int8
)  # stealing name of a built-in function
rooms = make_rooms()
for room in rooms:
    draw_room(map)


def draw_horiz_passage(i, j, map):
    assert i < j
    assert i // GRID_COLS == j // GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, hj, _] = rooms[j]
    yi = yi + randint(1, hi - 2)
    yj = yj + randint(1, hj - 2)
    map[yi, xi + wi - 1] = ord("+")
    map[yj, xj] = ord("+")
    draw_passage(yi, xi + wi, yj, xj - 1, map)


def draw_vert_passage(i, j, map):
    assert i < j
    assert i % GRID_COLS == j % GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, hj, wj] = rooms[j]
    xi = xi + randint(1, wi - 2)
    xj = xj + randint(1, wj - 2)
    map[yi + hi - 1, xi] = ord("+")
    map[yj, xj] = ord("+")

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
        map[yprev : y + 1, x] = ord("#")
        yprev = y
        x += s


def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    mapwin = curses.newwin(
        ROWS, COLS
    )  # map only takes up first 23 rows, curses issue with bottom right character of window

    for i, j in [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8)]:
        draw_horiz_passage(i, j, map)

    for i, j in [(0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8)]:
        draw_vert_passage(i, j, map)

    mapwin.addstr(map.tobytes())
    stdscr.refresh()
    mapwin.refresh()

    stdscr.getkey()


curses.wrapper(main)
