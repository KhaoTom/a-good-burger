import numpy
import random
import tcod
from game.entity import spawn
from game.datatypes import Dungeon, Rectangle


def generate_dungeon(
        max_rooms,
        room_min_size,
        room_max_size,
        map_width,
        map_height,
        player,
        max_entities_per_room,
        floor_tile,
        wall_tile
):
    """ Basic dungeon generator. """
    dungeon = Dungeon(
        width=map_width,
        height=map_height,
        entities={player},
        tiles=numpy.full((map_width, map_height), fill_value=wall_tile, order="F"),
        visible=numpy.full((map_width, map_height), fill_value=False, order="F"),
        explored=numpy.full((map_width, map_height), fill_value=False, order="F"),
    )

    rooms: list[Rectangle] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = Rectangle(x, y, room_width, room_height)

        if any(rectangle_intersects(new_room, other_room) for other_room in rooms):
            continue

        dungeon.tiles[rectangle_inner(new_room)] = floor_tile

        if len(rooms) == 0:
            player.x, player.y = rectangle_center(new_room)
        else:
            for x, y in tunnel_between(rectangle_center(rooms[-1]), rectangle_center(new_room)):
                dungeon.tiles[x, y] = floor_tile

        place_entities(new_room, dungeon, max_entities_per_room)

        rooms.append(new_room)

    return dungeon


def place_entities(room, dungeon, max_entities_to_place):
    number_of_placement_attempts = random.randint(0, max_entities_to_place)

    for i in range(number_of_placement_attempts):
        x = random.randint(room.x1 + 1, room.x2 - 1)
        y = random.randint(room.y1 + 1, room.y2 - 1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            entity_chosen = random.choices(['orc', 'troll', 'patty'], weights=[4, 1, 1], k=1)[0]
            dungeon.entities.add(spawn(entity_chosen, x, y))


def tunnel_between(start, end):
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


def rectangle_center(rect):
    center_x = int((rect.x1 + rect.x2) / 2)
    center_y = int((rect.y1 + rect.y2) / 2)
    return center_x, center_y


def rectangle_inner(rect):
    return slice(rect.x1+1, rect.x2), slice(rect.y1+1, rect.y2)


def rectangle_intersects(rect1, rect2):
    return (
        rect1.x1 <= rect2.x2
        and rect1.x2 >= rect2.x1
        and rect1.y1 <= rect2.y2
        and rect1.y2 >= rect2.y1
    )


def get_path_to(dungeon, acting_entity, dest_x, dest_y):
    cost = numpy.array(dungeon.tiles["walkable"], dtype=numpy.int8)

    for entity in dungeon.entities:
        if entity.blocks_movement and cost[entity.x, entity.y]:
            cost[entity.x, entity.y] += 10

    graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
    pathfinder = tcod.path.Pathfinder(graph)
    pathfinder.add_root((acting_entity.x, acting_entity.y))
    path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()
    return path


def update_fov(dungeon, x, y):
    dungeon.visible[:] = tcod.map.compute_fov(
        dungeon.tiles["transparent"],
        (x, y),
        radius=8
    )
    dungeon.explored |= dungeon.visible
