import tcod
from game import tiletypes
from game.dungeon import generate_dungeon, update_fov
from game.entity import spawn, is_alive
from game.keybind import KEYBINDS
from game.render import render_map, render_messagebar, render_statusbar
from game.simulation import process_turn


def main():
    player = spawn('player', 0, 0)

    dungeon = generate_dungeon(
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
    update_fov(dungeon, player.x, player.y)

    messages = ['Welcome to "A Good Burger"!']
    show_message_on_next_render = True
    message_index = -1

    turn_count = 0

    console = tcod.Console(80, 50, order="F")
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tcod.tileset.load_tilesheet("assets/Tiles_12x12.png", 16, 16, tcod.tileset.CHARMAP_CP437),
        title="A Good Burger",
        vsync=True,
    ) as context:
        while True:
            console.clear()

            render_map(dungeon, console)
            render_statusbar(player, turn_count, console)

            if show_message_on_next_render:
                render_messagebar(messages, message_index, console)

            context.present(console)

            events = tcod.event.wait()

            for event in events:
                context.convert_event(event)
                match event:
                    case tcod.event.Quit():
                        raise SystemExit()

                    case tcod.event.KeyDown(sym=sym):
                        action = KEYBINDS.get(sym)
                        if action is None:
                            continue

                        if action == "EXIT":
                            raise SystemExit()

                        if action == "SCROLL_MESSAGES":
                            message_index = message_index - 1 if abs(message_index) < len(messages) else -len(messages)
                            show_message_on_next_render = True
                            continue

                        if not is_alive(player):
                            continue

                        turn_processed, new_messages = process_turn(dungeon, player, action, turn_count)
                        if turn_processed:
                            update_fov(dungeon, player.x, player.y)
                            show_message_on_next_render = False
                            turn_count += 1

                        if len(new_messages) > 0:
                            messages += new_messages
                            message_index = -1
                            show_message_on_next_render = True


if __name__ == "__main__":
    main()
