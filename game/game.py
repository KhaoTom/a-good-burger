from game import Z_CORPSE


def melee(entity, target):
    attack = entity.stats["attack"]
    defense = target.stats["defense"]
    damage = attack.current_value - defense.current_value

    attack_desc = f"{entity.name.capitalize()} attacks {target.name}"

    target_hp = target.stats["hp"]
    if target_hp.is_at_minimum():
        print(f"{attack_desc}. It's already dead!")

    elif damage > 0:
        print(f"{attack_desc} for {damage} hit points.")
        target_hp.modify(-damage)
        if target_hp.is_at_minimum():
            kill(target)

    else:
        print(f"{attack_desc} but does no damage.")


def kill(target):
    print(f"{target.name.capitalize()} dies.")
    target.ai = None
    target.char = "%"
    target.color = (191, 0, 0)
    target.blocks_movement = False
    target.name = f"remains of {target.name}"
    target.z = Z_CORPSE


def move(entity, delta_x, delta_y):
    entity.x += delta_x
    entity.y += delta_y


def is_alive(entity):
    return entity.stats["hp"].current_value > entity.stats["hp"].minimum_value
