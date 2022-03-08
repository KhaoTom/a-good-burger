import random
import tcod
from game import entitytypes
from framework.gamemap import GameMap


class RectangularRoom:
    def __init__(self, x, y, width, height):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    @property
    def inner(self):
        return slice(self.x1+1, self.x2), slice(self.y1+1, self.y2)

    def intersects(self, other):
        """
        True if this room intersects other room
        :param other: room-like with x1, y1, x2, y2 positions
        :return: Bool
        """
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )


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

    rooms: list[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width - 1)
        y = random.randint(0, dungeon.height - room_height - 1)

        new_room = RectangularRoom(x, y, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = floor_tile

        if len(rooms) == 0:
            player.x, player.y = new_room.center
        else:
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = floor_tile

        place_entities(new_room, dungeon, max_monsters_per_room)

        rooms.append(new_room)

    return dungeon