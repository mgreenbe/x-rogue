import curses
import state as s
from types_ import ICOL
import logging

logger = logging.getLogger()


def paint_screen(stdscr):
    stdscr.clear()

    if s.message is not None:
        stdscr.addstr(0, 0, s.message)
        stdscr.clrtoeol()

    active_items = s.items[s.items[:, ICOL.IS_ACTIVE] == 1]
    for symbol, pos in active_items[:, [ICOL.SYMBOL, ICOL.POS]]:
        y, x = pos >> 8, pos & 255
        stdscr.addch(y + 1, x, chr(symbol))

    pos = s.rogue["pos"]
    y, x = pos >> 8, pos & 255
    stdscr.addch(y + 1, x, "@", curses.color_pair(1) | curses.A_BOLD)

    level = s.level
    gold = s.rogue["gold"]
    hp = f"{s.rogue["hp"]}({s.rogue["max_hp"]})"
    str_ = f"{s.rogue["str"]}({s.rogue["max_str"]})"
    arm = s.rogue["arm"]
    exp = f"{s.rogue["exp_level"]}/{s.rogue["exp_points"]}"

    bottom_bar = f"Level: {level:<3}Gold: {gold:<7}Hp: {hp:<8}Str: {str_:<8}Arm: {arm:<4}Exp: {exp}"
    stdscr.addstr(24, 0, bottom_bar)

    stdscr.refresh()
