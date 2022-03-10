import numpy
import tcod

Z_PLAYER = 100
Z_NPC = 50
Z_CORPSE = 1


def melee(entity, target, messages):
    damage = entity.attack.current_value - target.defense.current_value

    attack_desc = f"{entity.name.capitalize()} attacks {target.name}"

    if target.hp.is_at_minimum():
        messages.append(f"{attack_desc}. It's already dead!")

    elif damage > 0:
        messages.append(f"{attack_desc} for {damage} hit points.")
        target.hp.modify(-damage)
        if target.hp.is_at_minimum():
            messages.append(f"{target.name.capitalize()} dies.")
            kill(target)

    else:
        messages.append(f"{attack_desc} but does no damage.")


def kill(target):
    target.ai = False
    target.char = "%"
    target.color = (191, 0, 0)
    target.blocks_movement = False
    target.name = f"remains of {target.name}"
    target.z = Z_CORPSE


def move(entity, delta_x, delta_y):
    entity.x += delta_x
    entity.y += delta_y


def is_alive(entity):
    return entity.hp.current_value > entity.hp.minimum_value


def handle_ai_turns(game_map, player, messages):
    player_died = False
    ai_entities = [e for e in game_map.entities - {player} if e.ai]
    for entity in ai_entities:

        target = player
        delta_x = target.x - entity.x
        delta_y = target.y - entity.y
        distance = max(abs(delta_x), abs(delta_y))  # Chebyshev distance.

        if game_map.visible[entity.x, entity.y]:
            if distance <= 1:
                handle_movement(game_map, entity, delta_x, delta_y, messages)
                continue

            entity.path = get_path_to(game_map, entity, target.x, target.y)

        if entity.path:
            dest_x, dest_y = entity.path.pop(0)
            delta_x = dest_x - entity.x
            delta_y = dest_y - entity.y
            handle_movement(game_map, entity, delta_x, delta_y, messages)
            continue

        if not is_alive(player):
            player_died = True
            break

    return player_died


def handle_movement(game_map, entity, delta_x, delta_y, messages):
    destination_x = entity.x + delta_x
    destination_y = entity.y + delta_y

    if not (0 <= destination_x < game_map.width and 0 <= destination_y < game_map.height):
        return
    if not game_map.tiles["walkable"][destination_x, destination_y]:
        return

    def entity_is_blocking_destination(_e):
        return _e.blocks_movement and _e.x == destination_x and _e.y == destination_y

    blocking_entity = next(filter(entity_is_blocking_destination, game_map.entities), None)

    if blocking_entity is None:
        move(entity, delta_x, delta_y)
    else:
        melee(entity, blocking_entity, messages)


def get_path_to(gamemap, acting_entity, dest_x, dest_y):
    cost = numpy.array(gamemap.tiles["walkable"], dtype=numpy.int8)

    for entity in gamemap.entities:
        if entity.blocks_movement and cost[entity.x, entity.y]:
            cost[entity.x, entity.y] += 10

    graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
    pathfinder = tcod.path.Pathfinder(graph)
    pathfinder.add_root((acting_entity.x, acting_entity.y))
    path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()
    return path


def update_fov(gamemap, x, y):
    gamemap.visible[:] = tcod.map.compute_fov(
        gamemap.tiles["transparent"],
        (x, y),
        radius=8
    )
    gamemap.explored |= gamemap.visible
