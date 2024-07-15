import state as s
from constants import COLORS, POTIONS

potion_colors = s.rng.choice(COLORS, size=len(POTIONS), replace=False)
