from game.entity import Entity
from game.constants import *


player = Entity(0, 0, Z_PLAYER, "@", (255, 255, 255), "Player", True, 30, 5, 2, False, None)

orc = Entity(0, 0, Z_NPC, "o", (63, 127, 63), "Orc", True, 10, 3, 0, True, None)
troll = Entity(0, 0, Z_NPC, "T", (0, 127, 0), "Troll", True, 16, 4, 1, True, None)
