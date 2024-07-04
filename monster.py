from typing import List, Literal, Tuple, TypedDict


class MonsterType(TypedDict):
    type: (
        Literal["kestrel"]
        | Literal["emu"]
        | Literal["snake"]
        | Literal["bat"]
        | Literal["hobgoblin"]
        | Literal["ice monster"]
        | Literal["rattlesnake"]
        | Literal["orc"]
        | Literal["zombie"]
    )
    symbol: str
    level: int
    armor: int
    damage: int


class Monster(MonsterType):
    id: int
    max_hp: int
    hp: int
    pos: Tuple[int, int]


monster_types: List[MonsterType] = [
    dict(type="kestrel", symbol=ord("K"), level=1, armor=7, damage=4),
    dict(type="emu", symbol=ord("E"), level=1, armor=7, damage=2),
    dict(type="snake", symbol=ord("S"), level=1, armor=5, damage=3),
    dict(type="bat", symbol=ord("B"), level=1, armor=3, damage=2),
    dict(type="hobgoblin", symbol=ord("H"), level=1, armor=5, damage=8),
    dict(type="ice monster", symbol=ord("I"), level=1, armor=9, damage=0),
    dict(type="rattlesnake", symbol=ord("R"), level=2, armor=3, damage=6),
    dict(type="orc", symbol=ord("O"), level=1, armor=6, damage=8),
    dict(type="zombie", symbol=ord("Z"), level=2, armor=8, damage=8),
]
