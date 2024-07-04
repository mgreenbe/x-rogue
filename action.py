# player action (keyboard input and response)
# getch

# wake monster(s) if previous room != current room
# changes status from idle to chase
# on movement (or start level or teleport update previous/current room)


from typing import List, Literal, TypedDict


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
    max_hp: int
    hp: int


class GoldType(TypedDict):
    type: Literal["Gold"]
    symbol: Literal[":"]


class Gold(GoldType):
    amount: int


damage = {
    "mace": (2, 4),
    "long sword": (3, 4),
    "dagger": (1, 6),
    "two-handed sword": (4, 4),
    "spear": (2, 3),
}

monster_types: List[MonsterType] = [
    dict(type="kestrel", symbol="K", level=1, armor=7, damage=4),
    dict(type="emu", symbol="E", level=1, armor=7, damage=2),
    dict(type="snake", symbol="S", level=1, armor=5, damage=3),
    dict(type="bat", symbol="B", level=1, armor=3, damage=2),
    dict(type="hobgoblin", symbol="H", level=1, armor=5, damage=8),
    dict(type="ice monster", symbol="I", level=1, armor=9, damage=0),
    dict(type="rattlesnake", symbol="R", level=2, armor=3, damage=6),
    dict(type="orc", symbol="O", level=1, armor=6, damage=8),
    dict(type="zombie", symbol="Z", level=2, armor=8, damage=8),
]
