import tcod

from game import entitytypes
from game import hacks
from game.states import MainState
from game.eventdispatcher import EventDispatcher
from game.mapgen import generate_dungeon
from game.tiletypes import floor, wall, unexplored


def main():
    hacks.apply_patches()

    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    tileset = tcod.tileset.load_tilesheet("assets/dejavu10x10_gs_tc_brighter.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_dispatcher = EventDispatcher()

    player = entitytypes.player.clone(0, 0)

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

    states = [MainState()]

    state_data = {
        "event_dispatcher": event_dispatcher,
        "game_map": game_map,
        "player": player
    }
    states[0].enter_state(state_data)

    current_state = states[0]

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="A Good Burger",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        while True:
            current_state.render(console=root_console, context=context)

            events = tcod.event.wait()
            current_state.update(events)


if __name__ == "__main__":
    main()
