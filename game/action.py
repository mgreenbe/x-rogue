import logging
import state as s
from queue import PriorityQueue
from types_ import A, C, D, I, K, ICOL
import numpy as np
from constants import POSITIONS, POTIONS
from randomized import potion_colors

logger = logging.getLogger()

action_queue = PriorityQueue()
action_queue.put((-1, A.NEXT_LEVEL, None))
action_queue.put((0, A.GET_COMMAND, None))


def clear_message_on_next_paint():
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
            s.items[:] = 0
            n = 40
            s.items[:n, ICOL.TYPE] = I.GOLD
            s.items[n : 2 * n, ICOL.TYPE] = I.POTION
            s.items[n : 2 * n, ICOL.SUBTYPE] = s.rng.choice(len(POTIONS), size=n)
            s.items[:n, ICOL.SYMBOL] = ord("*")
            s.items[n : 2 * n, ICOL.SYMBOL] = ord("?")
            s.items[:n, ICOL.QUANTITY] = s.rng.integers(10, 100, size=n)
            s.items[: 2 * n, ICOL.IS_ACTIVE] = 1
            s.items[: 2 * n, ICOL.POS] = s.rng.choice(
                POSITIONS, size=2 * n, replace=False
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
            clear_message_on_next_paint()
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
                    case C.SPACE:
                        queue_up(A.GET_COMMAND)
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
                    case C.DOWN | C.j:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.S, "reps": reps},
                        )
                    case C.UP | C.k:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.N, "reps": reps},
                        )
                    case C.LEFT | C.h:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.W, "reps": reps},
                        )
                    case C.RIGHT | C.l:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.E, "reps": reps},
                        )
                    case C.b:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.SW, "reps": reps},
                        )
                    case C.n:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.SE, "reps": reps},
                        )
                    case C.y:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.NW, "reps": reps},
                        )
                    case C.u:
                        queue_up(
                            A.MOVE_ROGUE,
                            payload={"dir": D.NE, "reps": reps},
                        )
        # --------------------------------------------------------------------MOVE_ROGUE
        case A.MOVE_ROGUE:
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
                case D.SW:
                    x -= 1
                    y += 1
                case D.SE:
                    x += 1
                    y += 1
                case D.NW:
                    x -= 1
                    y -= 1
                case D.NE:
                    x += 1
                    y -= 1
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
            assert np.sum(s.items[:, ICOL.POS] == pos) == 1
            i = np.argmax(s.items[:, ICOL.POS] == pos)
            assert s.items[i, ICOL.POS] == pos
            match s.items[i, ICOL.TYPE]:
                case I.GOLD:
                    gold = s.items[i, ICOL.QUANTITY]
                    s.rogue["gold"] += gold
                    s.message_queue.put(f"You found {gold} gold pieces.")
                case I.POTION:
                    color = potion_colors[s.items[i, ICOL.SUBTYPE]]
                    article = "an" if color[0] in "aeiou" else "a"
                    s.message_queue.put(f"You found {article} {color} potion.")
                    # TODO: Inventory!
            s.items[i, ICOL.IS_ACTIVE] = 0
        # ------------------------------------------------------------------CONFIRM_QUIT
        case A.CONFIRM_QUIT:
            clear_message_on_next_paint()
            c = stdscr.getch()
            logger.info(f"c = {c}")
            if c == K.Y or c == K.y:
                return True  # done, break out of game loop
            else:
                queue_up(A.GET_COMMAND)
