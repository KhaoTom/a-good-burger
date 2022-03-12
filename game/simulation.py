from game.dungeon import get_path_to
from game.entity import is_alive, move, melee


def process_turn(dungeon, player, player_action, turn_count):
    messages = []
    turn_processed = False

    match player_action:
        case "WAIT":
            messages += [f"{turn_count}: {msg}" for msg in handle_ai_turns(dungeon, player)]
            turn_processed = True

        case (delta_x, delta_y):
            is_valid_move, move_msgs = handle_movement(dungeon, player, delta_x, delta_y)
            messages += [f"{turn_count}: {msg}" for msg in move_msgs]
            if is_valid_move:
                messages += [f"{turn_count}: {msg}" for msg in handle_ai_turns(dungeon, player)]
                turn_processed = True

    return turn_processed, messages


def handle_ai_turns(dungeon, player):
    messages = []
    ai_entities = [e for e in dungeon.entities - {player} if e.ai]
    for entity in ai_entities:

        target = player
        delta_x = target.x - entity.x
        delta_y = target.y - entity.y
        distance = max(abs(delta_x), abs(delta_y))

        if dungeon.visible[entity.x, entity.y]:
            if distance <= 1:
                _, msgs = handle_movement(dungeon, entity, delta_x, delta_y)
                messages += msgs
                continue

            entity.path = get_path_to(dungeon, entity, target.x, target.y)

        if entity.path:
            dest_x, dest_y = entity.path.pop(0)
            delta_x = dest_x - entity.x
            delta_y = dest_y - entity.y
            _, msgs = handle_movement(dungeon, entity, delta_x, delta_y)
            messages += msgs
            continue

        if not is_alive(player):
            break

    return messages


def handle_movement(dungeon, entity, delta_x, delta_y):
    messages = []

    destination_x = entity.x + delta_x
    destination_y = entity.y + delta_y

    if not (0 <= destination_x < dungeon.width and 0 <= destination_y < dungeon.height):
        return False, messages
    if not dungeon.tiles["walkable"][destination_x, destination_y]:
        return False, messages

    def entity_at_destination(_e):
        return _e.x == destination_x and _e.y == destination_y

    entities_at_destination = list(filter(entity_at_destination, dungeon.entities))
    if entities_at_destination:

        def entity_is_blocking_destination(_e):
            return _e.blocks_movement

        blocking_entity = next(filter(entity_is_blocking_destination, entities_at_destination), None)

        if blocking_entity is None:
            move(entity, delta_x, delta_y)
        else:
            messages += melee(entity, blocking_entity)
    else:
        move(entity, delta_x, delta_y)

    return True, messages
