from enum import Enum, IntEnum

# import numpy as np

A = Enum(
    "ACTION",
    [
        "PASS",
        "NEXT_LEVEL",
        "GET_COMMAND",
        "CONFIRM_QUIT",
        "MOVE_ROGUE",
        "PICK_UP",
        "DISPLAY_MESSAGES",
        "PROMPT_FOR_NEXT_MESSAGE",
        "ROGUE_TURN",
        "LAST_MESSAGE",
    ],
)

# Directions
D = Enum("DIR", ["S", "N", "W", "E"])

# ITEMS
I = IntEnum("Item", ["ARMOR", "WEAPON", "SCROLL", "POTION", "GOLD", "FOOD"])


# Item matrix columns
class ICOL(IntEnum):
    TYPE = 0
    SYMBOL = 1
    GOLD = 2
    POS = 3


# Commands
class C(IntEnum):
    CTRL_C = 3
    CTRL_P = 16
    TWO = 50
    THREE = 51
    FOUR = 52
    FIVE = 53
    SIX = 54
    SEVEN = 55
    EIGHT = 56
    NINE = 57
    Q = 81
    DOWN = 258
    UP = 259
    LEFT = 260
    RIGHT = 261


# Keys
class K(IntEnum):
    SPACE = 32
    Y = 89
    y = 121


# item_dtype = np.dtype(
#     [("item_type", int), ("symbol", int), ("gold", int), ("pos", int)]
# )
