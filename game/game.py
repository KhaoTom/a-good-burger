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


def handle_ai_turns(game_map, player):
    player_died = False
    ai_entities = [e for e in game_map.entities - {player} if e.ai]
    for entity in ai_entities:

        target = player
        delta_x = target.x - entity.x
        delta_y = target.y - entity.y
        distance = max(abs(delta_x), abs(delta_y))  # Chebyshev distance.

        if game_map.visible[entity.x, entity.y]:
            if distance <= 1:
                handle_movement(game_map, entity, delta_x, delta_y)
                continue

            entity.path = game_map.get_path_to(entity, target.x, target.y)

        if entity.path:
            dest_x, dest_y = entity.path.pop(0)
            delta_x = dest_x - entity.x
            delta_y = dest_y - entity.y
            handle_movement(game_map, entity, delta_x, delta_y)
            continue

        if not is_alive(player):
            player_died = True
            break

    return player_died


def handle_movement(game_map, entity, delta_x, delta_y):
    new_x = entity.x + delta_x
    new_y = entity.y + delta_y

    if not game_map.in_bounds(new_x, new_y):
        return
    if not game_map.tiles["walkable"][new_x, new_y]:
        return

    target = game_map.get_blocking_entity_at(new_x, new_y)
    if target is None:
        move(entity, delta_x, delta_y)
    else:
        melee(entity, target)
