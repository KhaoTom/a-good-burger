import copy

from game.datatypes import Entity


Z_PLAYER = 100
Z_NPC = 50
Z_ITEM = 10
Z_CORPSE = 1


entity_templates = {
    "player": Entity(0, 0, Z_PLAYER, "@", (255, 255, 255), "Player", True, 30, 5, 2, False, None),
    # monsters
    "orc": Entity(0, 0, Z_NPC, "o", (63, 127, 63), "Orc", True, 10, 3, 0, True, None),
    "troll": Entity(0, 0, Z_NPC, "T", (0, 127, 0), "Troll", True, 16, 4, 1, True, None),
    # items
    "patty": Entity(0, 0, Z_ITEM, "$", (100, 100, 50), "burger patty", False, 4, 0, 0, False, None),
}


def spawn(entity_name, x, y):
    entity = entity_templates[entity_name]
    clone = copy.deepcopy(entity)
    clone.x = x
    clone.y = y
    return clone


def melee(entity, target):
    messages = []
    damage = entity.attack - target.defense

    attack_desc = f"{entity.name.capitalize()} attacks {target.name}"

    if target.hp <= 0:
        messages.append(f"{attack_desc}. It's already dead!")

    elif damage > 0:
        messages.append(f"{attack_desc} for {damage} hit points.")
        target.hp -= damage
        if target.hp <= 0:
            messages.append(f"{target.name.capitalize()} dies.")
            kill(target)

    else:
        messages.append(f"{attack_desc} but does no damage.")

    return messages


def kill(entity):
    entity.ai = False
    entity.char = "%"
    entity.color = (191, 0, 0)
    entity.blocks_movement = False
    entity.name = f"remains of {entity.name}"
    entity.z = Z_CORPSE


def move(entity, delta_x, delta_y):
    entity.x += delta_x
    entity.y += delta_y


def is_alive(entity):
    return entity.hp > 0

