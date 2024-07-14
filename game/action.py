import logging
import state as s
from queue import PriorityQueue
from types_ import A, C, D, I, K, ICOL
import numpy.ma as ma
import numpy as np

logger = logging.getLogger()

action_queue = PriorityQueue()
action_queue.put((-1, A.NEXT_LEVEL, None))
action_queue.put((0, A.GET_COMMAND, None))


def clear_message():
    if s.message != None:
        s.previous_message = s.message
    s.message = None


def queue_up(action_type, time=None, payload=None):
    time = time or s.time
    action_queue.put((time, action_type, payload))


def take_action(stdscr):
    s.time, action_type, payload = action_queue.get()
    logger.info(
        f"---\n     s.time = {s.time}\naction_type = {action_type.name}\n    payload = {payload}"
    )
    match action_type:
        # --------------------------------------------------------------------------PASS
        case A.PASS:
            pass
        # --------------------------------------------------------------------NEXT_LEVEL
        case A.NEXT_LEVEL:
            s.level += 1
            s.items[:] = ma.masked
            n = 50
            s.items[:n, ICOL.TYPE] = I.GOLD
            s.items[:n, ICOL.SYMBOL] = ord("*")
            s.items[:n, ICOL.GOLD] = s.rng.integers(10, 100, size=n)
            s.items[:n, ICOL.POS] = (s.rng.integers(23, size=n) << 8) + s.rng.integers(
                80, size=n
            )
        # --------------------------------------------------------------DISPLAY_MESSAGES
        case A.DISPLAY_MESSAGES:
            message = s.message_queue.get()
            logger.info(message)
            if not s.message_queue.empty():
                s.message = message + "--MORE--"
                queue_up(A.PROMPT_FOR_NEXT_MESSAGE, payload=payload)
            else:
                s.message = message
                queue_up(A.GET_COMMAND, payload=payload)
        # -------------------------------------------------------PROMPT_FOR_NEXT_MESSAGE
        case A.PROMPT_FOR_NEXT_MESSAGE:
            c = 0
            while c != K.SPACE:
                c = stdscr.getch()
                logger.info(f"c = {c}")
            queue_up(A.DISPLAY_MESSAGES, payload=payload)
        # -------------------------------------------------------------------GET_COMMAND
        case A.GET_COMMAND:
            if not s.message_queue.empty():  # display messages in queue
                queue_up(A.DISPLAY_MESSAGES, payload=payload)
            else:
                reps = 1 if payload is None else payload["reps"]
                c = 0
                while c not in C:
                    c = stdscr.getch()
                    logger.info(f"c = {c}")
                match c:
                    case C.CTRL_C | C.Q:
                        s.message = "Really quit?"
                        queue_up(A.CONFIRM_QUIT)
                    case C.CTRL_P:
                        s.message = s.previous_message
                        queue_up(A.GET_COMMAND, payload=payload)
                    case (
                        C.TWO
                        | C.THREE
                        | C.FOUR
                        | C.FIVE
                        | C.SIX
                        | C.SEVEN
                        | C.EIGHT
                        | C.NINE
                    ):
                        logger.info(f"Next command will be repeated {c - 48} times.")
                        queue_up(A.GET_COMMAND, payload={"reps": c - 48})
                    case C.DOWN | C.UP | C.LEFT | C.RIGHT:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D(c - 257), "reps": reps},
                        )
        # --------------------------------------------------------------------MOVE_ROGUE
        case A.MOVE_ROGUE:
            clear_message()
            if payload is not None:
                reps = 1 if payload is None else payload["reps"]
            pos = s.rogue["pos"]
            y, x = pos >> 8, pos & 255
            match payload["dir"]:
                case D.S:
                    y += 1
                case D.N:
                    y -= 1
                case D.W:
                    x -= 1
                case D.E:
                    x += 1
            pos = (y << 8) + x
            s.rogue["pos"] = pos
            pick_up = pos in s.items[:, ICOL.POS]
            if pick_up:
                queue_up(A.PICK_UP, time=s.time + 1)  # pick up next turn
            if reps == 1:
                queue_up(A.GET_COMMAND, time=s.time + pick_up + 1)
            else:
                assert isinstance(reps, int) and reps > 1
                queue_up(
                    A.MOVE_ROGUE,
                    time=s.time + pick_up + 1,
                    payload={"dir": payload["dir"], "reps": reps - 1},
                )
        # -----------------------------------------------------------------------PICK_UP
        case A.PICK_UP:
            pos = s.rogue["pos"]
            i = np.argmax(s.items[:, ICOL.POS] == pos)
            assert s.items[i, ICOL.POS] == pos
            gold = s.items[i, ICOL.GOLD]
            s.rogue["gold"] += gold
            s.items[i] = ma.masked
            s.message_queue.put(f"You found {gold} gold pieces.")
        # ------------------------------------------------------------------CONFIRM_QUIT
        case A.CONFIRM_QUIT:
            c = stdscr.getch()
            logger.info(f"c = {c}")
            if c == K.Y or c == K.y:
                return True
            else:
                clear_message()
                queue_up(A.GET_COMMAND)
