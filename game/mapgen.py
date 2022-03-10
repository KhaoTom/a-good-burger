import random
import tcod
from game import entitytypes
from game.gamemap import GameMap
from game.rectangle import *


def generate_dungeon(
        max_rooms,
        room_min_size,
        room_max_size,
        map_width,
        map_height,
        player,
        max_monsters_per_room,
        floor_tile,
        wall_tile,
        unexplored_tile
):
    """ Basic dungeon generator. """
    dungeon = GameMap(map_width, map_height, entities=[player], fill_tile=wall_tile, unexplored_tile=unexplored_tile)

    rooms: list[Rectangle] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = Rectangle(x, y, room_width, room_height)

        if any(intersects(new_room, other_room) for other_room in rooms):
            continue

        dungeon.tiles[inner(new_room)] = floor_tile

        if len(rooms) == 0:
            player.x, player.y = center(new_room)
        else:
            for x, y in tunnel_between(center(rooms[-1]), center(new_room)):
                dungeon.tiles[x, y] = floor_tile

        place_entities(new_room, dungeon, max_monsters_per_room)

        rooms.append(new_room)

    return dungeon


def place_entities(room, dungeon, maximum_monsters):
    number_of_monsters = random.randint(0, maximum_monsters)

    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                dungeon.entities.add(entitytypes.orc.clone(x, y))
            else:
                dungeon.entities.add(entitytypes.troll.clone(x, y))


def tunnel_between(start, end):
    """
    generator to dig an L shaped tunnel between points.
    :param start: (x, y) position to start at
    :param end: (x, y) position to end at
    :return: generator which yields x, y of next tile along tunnel at each iteration
    """
    x1, y1 = start
    x2, y2, = end

    if random.random() < 0.5:
        corner_x, corner_y = x2, y1
    else:
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y
