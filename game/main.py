import curses
import logging
from zmq.log.handlers import PUBHandler
from ui import paint_screen
from action import action_queue, take_action
import time


def main(stdscr):
    zmq_log_handler = PUBHandler("tcp://127.0.0.1:12345")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(zmq_log_handler)

    # time.sleep(1)

    curses.raw()
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)

    print("\x1B]0;X-ROGUE\x07")  # set title of terminal window

    while True:
        if action_queue.empty():
            raise Exception("Action queue is empty!")
        done = take_action(stdscr)
        if done:
            break
        paint_screen(stdscr)


curses.wrapper(main)
