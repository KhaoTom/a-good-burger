from entity import Entity
from engine import Engine
from constants import *


def init():
    # patching in custom functionality
    Entity.is_alive = _is_alive
    Entity.melee = _melee
    Engine.custom_render = _custom_render


# Class patches

def _custom_render(self, console):
    render_statusbar(self, console)


def _is_alive(self):
    return self.stats["hp"].current_value > self.stats["hp"].minimum_value


def _melee(self, target):
    attack = self.stats["attack"]
    defense = target.stats["defense"]
    damage = attack.current_value - defense.current_value

    attack_desc = f"{self.name.capitalize()} attacks {target.name}"

    target_hp = target.stats["hp"]
    if target_hp.is_at_minimum():
        print(f"{attack_desc}. It's already dead!")

    elif damage > 0:
        print(f"{attack_desc} for {damage} hit points.")
        target_hp.modify(-damage)
        if target_hp.is_at_minimum():
            kill_entity(target)

    else:
        print(f"{attack_desc} but does no damage.")


# Functionality

def kill_entity(target):
    print(f"{target.name.capitalize()} dies.")
    target.ai = None
    target.char = "%"
    target.color = (191, 0, 0)
    target.blocks_movement = False
    target.name = f"remains of {target.name}"
    target.z = Z_CORPSE


def render_statusbar(engine, console):
    player_hp = engine.player.stats["hp"]
    console.print(
        x=1,
        y=47,
        string=f"HP: {player_hp.current_value}/{player_hp.maximum_value}",
    )
