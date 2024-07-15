import numpy as np
import numpy.ma as ma
from rng import rng

__all__ = ["MonsterType", "monsters", "reset_monsters"]

_MAX_MONTERS = 100

_monster_dtype = np.dtype(
    [
        ("name", "S20"),
        ("symbol", int),
        ("exp_level", int),
        ("exp_points", int),
        ("damage", int),
        ("armor_class", int),
        ("pos", int, (2,)),
        ("hp", int),
        ("max_hp", int),
        ("is_asleep", bool),
    ]
)

_monster_type_dtype = np.dtype(
    [
        ("name", "S20"),
        ("symbol", int),
        ("exp_level", int),
        ("exp_points", int),
        ("damage", int),
        ("armor_class", int),
    ]
)

# fmt: off
_monster_types = np.array(
    [
    #    name,        symbol,   exp_level, exp_points, armor_class, damage
        ("kestrel",   ord("K"), 1,         2,          7,           4),
        ("emu",       ord("E"), 1,         2,          7,           2),
        ("snake",     ord("S"), 1,         2,          5,           3),
        ("bat",       ord("B"), 1,         2,          3,           2),
        ("hobgoblin", ord("H"), 1,         3,          5,           8),
        ("orc",       ord("O"), 1,         5,          6,           8),
        ("zombie",    ord("Z"), 2,         8,          8,           8),
    ],
    dtype=_monster_type_dtype
)
# fmt: on

monsters = ma.masked_all(_MAX_MONTERS, dtype=_monster_dtype)


def reset_monsters(n: int):
    monsters[:] = ma.masked
    for i in range(n):
        monster_type = rng.choice(_monster_types)
        exp_level = monster_type["exp_level"]
        hp = rng.integers(1, 9, size=exp_level).sum()
        max_hp = hp
        monsters[i] = (*monster_type, (0, 0), hp, max_hp, True)
