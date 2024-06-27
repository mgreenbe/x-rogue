from random import randint
from zmq.log.handlers import PUBHandler
import numpy as np
import random
import curses
import logging
import time

print("\x1B]0;X-ROGUE\x07")  # set title of terminal window

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
MIN_ROOM_WIDTH = 2
WALKABLE = (35, 43, 46)  # (ord("#"), ord("+"), ord("."))
SPACE = 32  # ord(" ")
STRUDEL = 64  # ord("@")

# random.seed(0)


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
        map[y, x : x + w] = ord("-")
        map[y + h - 1, x : x + w] = ord("-")
        map[y + 1 : y + h - 1, x] = ord("|")
        map[y + 1 : y + h - 1, x + w - 1] = ord("|")
        map[y + 1 : y + h - 1, x + 1 : x + w - 1] = ord(".")


def draw_horiz_passage(i, j, rooms, map):
    assert i < j
    assert i // GRID_COLS == j // GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, hj, _] = rooms[j]
    yi = yi + randint(1, hi - 2)
    yj = yj + randint(1, hj - 2)
    map[yi, xi + wi - 1] = ord("+")
    map[yj, xj] = ord("+")
    draw_passage(yi, xi + wi, yj, xj - 1, map)


def draw_vert_passage(i, j, rooms, map):
    assert i < j
    assert i % GRID_COLS == j % GRID_COLS
    [yi, xi, hi, wi] = rooms[i]
    [yj, xj, _, wj] = rooms[j]
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


def which_room(yhero, xhero, rooms):
    for i, [y, x, h, w] in enumerate(rooms):
        if y <= yhero and yhero < y + h and x <= xhero and xhero < x + w:
            return i


def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    mapwin = curses.newwin(
        ROWS, COLS
    )  # map only takes up first 23 rows, curses issue with bottom right character of window

    map = np.full(
        (ROWS - 1, COLS), SPACE, dtype=np.int8
    )  # stealing name of a built-in function
    mask = np.zeros_like(map)
    logger.info(mask.dtype)

    rooms = [make_room(i, j) for i in range(GRID_ROWS) for j in range(GRID_COLS)]
    draw_rooms(rooms, map)

    for i, j in [(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8)]:
        draw_horiz_passage(i, j, rooms, map)
    for i, j in [(0, 3), (1, 4), (2, 5), (3, 6), (4, 7), (5, 8)]:
        draw_vert_passage(i, j, rooms, map)

    # Put the hero in a random spot in a random room.
    [y, x, h, w] = random.choice(rooms)
    yhero = randint(y + 1, y + h - 2)
    xhero = randint(x + 1, x + w - 2)

    visited = set()
    while True:
        curroom = which_room(yhero, xhero, rooms)
        logger.info(
            "The hero is in "
            + ("a corridor." if curroom is None else f"room {curroom}.")
        )

        if curroom is not None and curroom not in visited:
            visited.add(curroom)
            [y, x, h, w] = rooms[curroom]
            mask[y : y + h, x : x + w] = 1

        mask[yhero - 1 : yhero + 2, xhero - 1 : xhero + 2] = 1

        mapcopy = map.copy()
        mapcopy[yhero, xhero] = STRUDEL
        mapcopy = mapcopy * mask + (1 - mask) * SPACE

        mapwin.addstr(0, 0, mapcopy.tobytes())
        stdscr.refresh()
        mapwin.refresh()
        key = stdscr.getkey()
        logger.info(key)
        if key == "KEY_UP" and (map[yhero - 1, xhero] in WALKABLE):
            yhero -= 1
        elif key == "KEY_DOWN" and (map[yhero + 1, xhero] in WALKABLE):
            yhero += 1
        if key == "KEY_LEFT" and (map[yhero, xhero - 1] in WALKABLE):
            xhero -= 1
        elif key == "KEY_RIGHT" and (map[yhero, xhero + 1] in WALKABLE):
            xhero += 1


curses.wrapper(main)
