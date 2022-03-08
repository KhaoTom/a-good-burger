from entity import Entity
from stats import Stat
from action import HostileAction


def _is_alive(self):
    return self.stats["hp"].current_value > self.stats["hp"].minimum_value


Entity.is_alive = _is_alive


def _make_stats(max_hp, attack, defense):
    stats = {
        "hp": Stat(0, max_hp, max_hp),
        "attack": Stat(0, attack, attack),
        "defense": Stat(0, defense, defense),
    }
    return stats


player = Entity(0, 0, "@", (255, 255, 255), "Player", True, _make_stats(30, 5, 2), None)

orc = Entity(0, 0, "o", (63, 127, 63), "Orc", True, _make_stats(10, 3, 0), HostileAction())
troll = Entity(0, 0, "T", (0, 127, 0), "Troll", True, _make_stats(16, 4, 1), HostileAction())
