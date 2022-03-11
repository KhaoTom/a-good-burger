from game.dungeon import get_path_to
from game.entity import is_alive, move, melee


def process_turn(dungeon, player, player_move, messages):
    match player_move:
        case None:
            return handle_ai_turns(dungeon, player, messages)
        case (delta_x, delta_y):
            handle_movement(dungeon, player, delta_x, delta_y, messages)
            return handle_ai_turns(dungeon, player, messages)


def handle_ai_turns(dungeon, player, messages):
    player_died = False
    ai_entities = [e for e in dungeon.entities - {player} if e.ai]
    for entity in ai_entities:

        target = player
        delta_x = target.x - entity.x
        delta_y = target.y - entity.y
        distance = max(abs(delta_x), abs(delta_y))

        if dungeon.visible[entity.x, entity.y]:
            if distance <= 1:
                handle_movement(dungeon, entity, delta_x, delta_y, messages)
                continue

            entity.path = get_path_to(dungeon, entity, target.x, target.y)

        if entity.path:
            dest_x, dest_y = entity.path.pop(0)
            delta_x = dest_x - entity.x
            delta_y = dest_y - entity.y
            handle_movement(dungeon, entity, delta_x, delta_y, messages)
            continue

        if not is_alive(player):
            player_died = True
            break

    return player_died


def handle_movement(dungeon, entity, delta_x, delta_y, messages):
    destination_x = entity.x + delta_x
    destination_y = entity.y + delta_y

    if not (0 <= destination_x < dungeon.width and 0 <= destination_y < dungeon.height):
        return
    if not dungeon.tiles["walkable"][destination_x, destination_y]:
        return

    def entity_is_blocking_destination(_e):
        return _e.blocks_movement and _e.x == destination_x and _e.y == destination_y

    blocking_entity = next(filter(entity_is_blocking_destination, dungeon.entities), None)

    if blocking_entity is None:
        move(entity, delta_x, delta_y)
    else:
        melee(entity, blocking_entity, messages)
