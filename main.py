from random import randint
from zmq.log.handlers import PUBHandler
import numpy as np
import random
import curses
import logging
import time
from level import Level
from constants import *

print("\x1B]0;X-ROGUE\x07")  # set title of terminal window

zmq_log_handler = PUBHandler("tcp://127.0.0.1:12345")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(zmq_log_handler)
time.sleep(0.5)
logger.info(f"x-rogue started, log level {logger.level}")

# random.seed(0)


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

    rng = np.random.default_rng()
    level = Level(rng)
    # rooms, map, monsters = make_level()

    curmap = level.map.copy()
    curmap[level.monsters.y, level.monsters.x] = level.monsters.symbol

    # Put the hero in a random spot in a random room.
    # Make sure there's no monster there.
    while True:
        [y, x, h, w] = random.choice(level.rooms)
        yhero = randint(y + 1, y + h - 2)
        xhero = randint(x + 1, x + w - 2)
        if all(np.logical_or(level.monsters.y != yhero, level.monsters.x != xhero)):
            break

    mask = np.zeros_like(level.map)

    visited = set()
    while True:
        curroom = which_room(yhero, xhero, level.rooms)
        logger.info(
            "The hero is in "
            + ("a corridor." if curroom is None else f"room {curroom}.")
        )
        if curroom is not None and curroom not in visited:
            visited.add(curroom)
            [y, x, h, w] = level.rooms[curroom]
            mask[y : y + h, x : x + w] = 1

        if level.map[yhero, xhero] == HASH or level.map[yhero, xhero] == PLUS:
            for y in [yhero - 1, yhero, yhero + 1]:
                for x in [xhero - 1, xhero, xhero + 1]:
                    if level.map[y, x] == HASH or level.map[y, x] == PLUS:
                        mask[y, x] = 1

        masked_map = curmap * mask + (1 - mask) * SPACE
        masked_map[yhero, xhero] = STRUDEL

        mapwin.addstr(0, 0, masked_map.tobytes())
        stdscr.refresh()
        mapwin.refresh()

        key = stdscr.getkey()
        logger.info(key)
        if key == "KEY_UP" and (level.map[yhero - 1, xhero] in WALKABLE):
            yhero -= 1
        elif key == "KEY_DOWN" and (level.map[yhero + 1, xhero] in WALKABLE):
            yhero += 1
        if key == "KEY_LEFT" and (level.map[yhero, xhero - 1] in WALKABLE):
            xhero -= 1
        elif key == "KEY_RIGHT" and (level.map[yhero, xhero + 1] in WALKABLE):
            xhero += 1


curses.wrapper(main)
