from typing import List, Tuple, TypedDict, Any
import numpy as np


class Game(TypedDict):
    depth: int
    map: np.ndarray
    rooms: List[Tuple[int, int, int, int]]
    items: List[Any]
    monsters: List[Any]
    stairs: Tuple[int, int]

    gold: int
    hitpoints: int
    max_hitpoints: int
    strength: int
    experience: int
    level: int
    inventory: List[Any]
    weapon: Any
    armor: Any
    rings: Tuple[int, int, int, int]
    hunger: int


monsters = [
    "aquator",
    "bat",
    "centaur",
    "dragon",
    "emu",
    "venus fly trap",
    "griffin",
    "hobgoblin",
    "ice monster",
    "jabberwock" "kestrel",
    "leprechaun",
    "medusa",
    "nymph",
    "orc",
    "phantom",
    "quagga",
    "rattlesnake",
    "snake",
    "troll",
    "black unicorn",
    "vampire",
    "wraith",
    "xeroc",
    "yeti",
    "zombie",
]
