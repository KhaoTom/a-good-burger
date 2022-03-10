import tcod
from game import entitytypes, mapgen, tiletypes, render, keybind, handle_movement, handle_ai_turns, update_fov


def main():
    player = entitytypes.player.clone(0, 0)

    game_map = mapgen.generate_dungeon(
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

            render.render_map(game_map, console)
            render.render_statusbar(player, console)

            if not messages_seen:
                render.render_messagebar(messages, console)

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
                        move_vector = keybind.MOVE_KEYS.get(sym)
                        if move_vector:
                            delta_x, delta_y = move_vector
                            handle_movement(game_map, player, delta_x, delta_y, new_messages)
                            player_dead = handle_ai_turns(game_map, player, new_messages)
                            update_fov(game_map, player.x, player.y)
                            messages_seen = True

                        elif sym in keybind.WAIT_KEYS:
                            player_dead = handle_ai_turns(game_map, player, new_messages)
                            update_fov(game_map, player.x, player.y)
                            messages_seen = True

                        if len(new_messages) > 0:
                            messages.append(new_messages)
                            messages_seen = False


if __name__ == "__main__":
    main()
