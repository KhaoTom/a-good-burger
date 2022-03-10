import tcod

from game import entitytypes
from game.mapgen import generate_dungeon
from game.tiletypes import floor, wall, unexplored
from game.render import *
from game.events import MOVE_KEYS, WAIT_KEYS
import game


def main():

    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("assets/dejavu10x10_gs_tc_brighter.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    player = entitytypes.player.clone(0, 0)
    player_died = False

    game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        player=player,
        max_monsters_per_room=max_monsters_per_room,
        floor_tile=floor,
        wall_tile=wall,
        unexplored_tile=unexplored
    )
    game_map.update_fov(player.x, player.y)

    console = tcod.Console(screen_width, screen_height, order="F")
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
        title="A Good Burger",
        vsync=True,
    ) as context:
        while True:
            render_map(game_map, console)
            render_statusbar(player, console)

            context.present(console)

            events = tcod.event.wait()

            for event in events:
                context.convert_event(event)  # Add tile coordinates to mouse events.
                match event:
                    case tcod.event.Quit():
                        raise SystemExit()

                    case tcod.event.KeyDown(sym=sym):
                        if not player_died:
                            if sym in MOVE_KEYS:
                                delta_x, delta_y = MOVE_KEYS[sym]
                                game.handle_movement(game_map, player, delta_x, delta_y)
                                player_died = game.handle_ai_turns(game_map, player)
                                game_map.update_fov(player.x, player.y)

                            elif sym in WAIT_KEYS:
                                player_died = game.handle_ai_turns(game_map, player)
                                game_map.update_fov(player.x, player.y)

                        if sym == tcod.event.K_ESCAPE:
                            raise SystemExit()


if __name__ == "__main__":
    main()
