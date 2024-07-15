from random import randint
from zmq.log.handlers import PUBHandler
import numpy as np
import curses
import logging
import time

# from level import Level
import level
from constants import *
import hero

print("\x1B]0;X-ROGUE\x07")  # set title of terminal window

zmq_log_handler = PUBHandler("tcp://127.0.0.1:12345")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(zmq_log_handler)
time.sleep(0.5)
logger.info(f"x-rogue started, log level {logger.level}")

#  clockwise starting from 3


def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    mapwin = curses.newwin(
        ROWS, COLS
    )  # map only takes up first 23 rows, curses issue with bottom right character of window
    statuswin = curses.newwin(1, COLS, 23, 0)

    rng = np.random.default_rng()
    level.init(rng)

    mask = np.zeros_like(level.map)
    turn = 0

    while True:
        logger.info(f"turn = {turn}")

        curmap = level.map.copy()
        for monster in level.monsters.itertuples(index=False):
            if (
                level.room_matrix[monster.y, monster.x]
                == level.room_matrix[hero.y, hero.x]
            ) or (np.abs(monster.y - hero.y) <= 1 and np.abs(monster.x - hero.x) <= 1):
                curmap[monster.y, monster.x] = monster.symbol

        logger.info(
            f"  The hero is at position ({hero.y}, {hero.x}) in "
            + ("a corridor." if hero.curroom is None else f"room {hero.curroom}.")
        )
        if hero.curroom != -1:
            [y, x, h, w] = level.rooms[hero.curroom]
            mask[y : y + h, x : x + w] = 1

        if level.map[hero.y, hero.x] == HASH or level.map[hero.y, hero.x] == PLUS:
            for y in [hero.y - 1, hero.y, hero.y + 1]:
                for x in [hero.x - 1, hero.x, hero.x + 1]:
                    if level.map[y, x] == HASH or level.map[y, x] == PLUS:
                        mask[y, x] = 1

        masked_map = curmap * mask + (1 - mask) * SPACE
        masked_map[hero.y, hero.x] = STRUDEL

        mapwin.addstr(0, 0, masked_map.tobytes())
        statuswin.addstr(0, 0, "Hi, mom!")
        stdscr.refresh()
        mapwin.refresh()
        statuswin.refresh()

        if turn % 2 == 0:
            for i, monster in level.monsters.iterrows():
                if monster.status == "chase":
                    bestdist = ROWS**2 + COLS**2
                    for dy, dx in [
                        (-1, -1),
                        (-1, 0),
                        (-1, 1),
                        (0, -1),
                        (0, 0),
                        (0, 1),
                        (1, -1),
                        (1, 0),
                        (1, 1),
                    ]:
                        curdist = (monster.y + dy - hero.y) ** 2 + (
                            monster.x + dx - hero.x
                        ) ** 2
                        if (
                            curdist < bestdist
                            and level.map[monster.y + dy, monster.x + dx] in WALKABLE
                            and (monster.y + dy != hero.y or monster.x + dx != hero.x)
                        ):
                            bestdy = dy
                            bestdx = dx
                            bestdist = curdist
                    logger.info(
                        f"bestdy = {bestdy}, bestdx = {bestdx}, bestdist = {bestdist}"
                    )
                    if bestdx != 0 or bestdy != 0:
                        logger.info(
                            f"  The {monster.type} at position ({monster.y}, {monster.x}) moves to position ({monster.y + dy}, {monster.x + dx})."
                        )
                        level.monsters.at[i, "y"] += bestdy
                        level.monsters.at[i, "x"] += bestdx
                        level.monsters.at[i, "curroom"] = level.room_matrix[
                            monster.y, monster.x
                        ]

                elif monster.curroom == hero.curroom:
                    logger.info(
                        f"  The {monster.type} at position ({monster.y}, {monster.x}) in room {monster.curroom} starts to chase you."
                    )
                    level.monsters.at[i, "status"] = "chase"
        else:
            key = stdscr.getkey()
            # logger.info(key)
            dy, dx = 0, 0
            if (key == "KEY_UP" or key == "8") and (
                level.map[hero.y - 1, hero.x] in WALKABLE
            ):
                dy, dx = -1, 0
                dx = 0
                hero.y -= 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)
            elif (key == "KEY_DOWN" or key == "2") and (
                level.map[hero.y + 1, hero.x] in WALKABLE
            ):
                dy, dx = 1, 0
                hero.y += 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)
            elif (key == "KEY_LEFT" or key == "4") and (
                level.map[hero.y, hero.x - 1] in WALKABLE
            ):
                dy, dx = 0, -1
                hero.x -= 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)
            elif (key == "KEY_RIGHT" or key == "6") and (
                level.map[hero.y, hero.x + 1] in WALKABLE
            ):
                dy, dx = 0, 1
                hero.x += 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)
            elif (
                key == "1"
                and level.map[hero.y, hero.x - 1] in WALKABLE
                and level.map[hero.y + 1, hero.x] in WALKABLE
                and level.map[hero.y + 1, hero.x - 1] in WALKABLE
            ):
                dy, dx = 1, -1
                hero.x -= 1
                hero.y += 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)
            elif (
                key == "3"
                and level.map[hero.y, hero.x + 1] in WALKABLE
                and level.map[hero.y + 1, hero.x] in WALKABLE
                and level.map[hero.y + 1, hero.x + 1] in WALKABLE
            ):
                dy, dx = 1, 1
                hero.x += 1
                hero.y += 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)
            elif (
                key == "7"
                and level.map[hero.y, hero.x - 1] in WALKABLE
                and level.map[hero.y - 1, hero.x] in WALKABLE
                and level.map[hero.y - 1, hero.x - 1] in WALKABLE
            ):
                dy, dy = -1, -1
                hero.x -= 1
                hero.y -= 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)
            elif (
                key == "9"
                and level.map[hero.y, hero.x + 1] in WALKABLE
                and level.map[hero.y - 1, hero.x] in WALKABLE
                and level.map[hero.y - 1, hero.x + 1] in WALKABLE
            ):
                dy, dx = 1, -1
                hero.x += 1
                hero.y -= 1
                curroom = level.room_matrix[hero.y, hero.x]
                hero.curroom = curroom
                level.visited_rooms.add(curroom)

            # if (dy != 0 or dx != 0) and (
            #     level.map[hero.y + dy, hero.x + dx] in WALKABLE
            # ):
            #     hero.x += 1
            #     hero.y -= 1
            #     curroom = level.room_matrix[hero.y, hero.x]
            #     hero.curroom = curroom
            #     level.visited_rooms.add(curroom)

        turn += 1


curses.wrapper(main)
