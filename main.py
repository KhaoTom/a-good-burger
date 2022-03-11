import tcod
from game import tiletypes
from game.dungeon import generate_dungeon, get_path_to, update_fov
from game.entity import spawn, is_alive, move, melee
from game.keybind import MOVE_KEYS, WAIT_KEYS
from game.render import render_map, render_messagebar, render_statusbar


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


def main():
    player = spawn('player', 0, 0)

    game_map = generate_dungeon(
        max_rooms=30,
        room_min_size=6,
        room_max_size=10,
        map_width=80,
        map_height=45,
        player=player,
        max_monsters_per_room=2,
        floor_tile=tiletypes.floor,
        wall_tile=tiletypes.wall
    )
    update_fov(game_map, player.x, player.y)

    player_dead = False
    messages = [['Welcome to "A Good Burger"!']]
    messages_seen = False

    console = tcod.Console(80, 50, order="F")
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tcod.tileset.load_tilesheet("assets/dejavu10x10_gs_tc_brighter.png", 32, 8, tcod.tileset.CHARMAP_TCOD),
        title="A Good Burger",
        vsync=True,
    ) as context:
        while True:
            console.clear()

            render_map(game_map, console)
            render_statusbar(player, console)

            if not messages_seen:
                render_messagebar(messages, console)

            context.present(console)

            events = tcod.event.wait()

            for event in events:
                context.convert_event(event)  # Add tile coordinates to mouse events.
                match event:
                    case tcod.event.Quit():
                        raise SystemExit()

                    case tcod.event.KeyDown(sym=sym):
                        if sym == tcod.event.K_ESCAPE:
                            raise SystemExit()

                        if player_dead:
                            continue

                        new_messages = []
                        move_vector = MOVE_KEYS.get(sym)
                        if move_vector:
                            delta_x, delta_y = move_vector
                            handle_movement(game_map, player, delta_x, delta_y, new_messages)
                            player_dead = handle_ai_turns(game_map, player, new_messages)
                            update_fov(game_map, player.x, player.y)
                            messages_seen = True

                        elif sym in WAIT_KEYS:
                            player_dead = handle_ai_turns(game_map, player, new_messages)
                            update_fov(game_map, player.x, player.y)
                            messages_seen = True

                        if len(new_messages) > 0:
                            messages.append(new_messages)
                            messages_seen = False


if __name__ == "__main__":
    main()
