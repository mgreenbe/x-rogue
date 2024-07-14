import numpy as np
import numpy.ma as ma
from queue import SimpleQueue
from types_ import ICOL


rng = np.random.default_rng()
time = 0
level = 0
message_queue = SimpleQueue()
message = "Welcome to X-Rogue!"
previous_message = None
rogue = {
    "pos": (11 << 8) + 40,
    "gold": 0,
    "hp": 12,
    "max_hp": 12,
    "str": 16,
    "max_str": 16,
    "arm": 4,
    "exp_level": 1,
    "exp_points": 0,
}
items = ma.masked_all((100, len(ICOL)), dtype=int)
