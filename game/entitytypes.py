from framework.entity import Entity
from framework.stats import BoundedStat
from game.action import HostileAction
from game.constants import *


def _make_stats(max_hp, attack, defense):
    stats = {
        "hp": BoundedStat(0, max_hp, max_hp),
        "attack": BoundedStat(0, attack, attack),
        "defense": BoundedStat(0, defense, defense),
    }
    return stats


player = Entity(0, 0, Z_PLAYER, "@", (255, 255, 255), "Player", True, _make_stats(30, 5, 2), None)

orc = Entity(0, 0, Z_NPC, "o", (63, 127, 63), "Orc", True, _make_stats(10, 3, 0), HostileAction())
troll = Entity(0, 0, Z_NPC, "T", (0, 127, 0), "Troll", True, _make_stats(16, 4, 1), HostileAction())
