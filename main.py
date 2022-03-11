import tcod
from game import tiletypes
from game.dungeon import generate_dungeon, update_fov
from game.entity import spawn, is_alive
from game.keybind import MOVE_KEYS, WAIT_KEYS
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
    messages_seen = False
    message_index = -1

    turn_count = 0

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

            render_map(dungeon, console)
            render_statusbar(player, console)

            if not messages_seen:
                render_messagebar(messages, message_index, console)

            context.present(console)

            events = tcod.event.wait()

            for event in events:
                context.convert_event(event)
                match event:
                    case tcod.event.Quit():
                        raise SystemExit()

                    case tcod.event.KeyDown(sym=sym):
                        if sym == tcod.event.K_ESCAPE:
                            raise SystemExit()

                        if sym == tcod.event.K_BACKSPACE:
                            message_index = message_index - 1 if abs(message_index) < len(messages) else -len(messages)
                            messages_seen = False
                            continue

                        if not is_alive(player):
                            continue

                        new_messages = []
                        move_vector = MOVE_KEYS.get(sym)
                        if move_vector:
                            new_messages += process_turn(dungeon, player, move_vector, turn_count)
                            update_fov(dungeon, player.x, player.y)
                            messages_seen = True
                            turn_count += 1

                        elif sym in WAIT_KEYS:
                            new_messages += process_turn(dungeon, player, None, turn_count)
                            update_fov(dungeon, player.x, player.y)
                            messages_seen = True
                            turn_count += 1

                        if len(new_messages) > 0:
                            messages += new_messages
                            message_index = -1
                            messages_seen = False


if __name__ == "__main__":
    main()
