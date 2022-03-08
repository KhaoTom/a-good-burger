import numpy
from framework import tiletype
import tcod


class GameMap:
    def __init__(self, width, height, entities):
        self.width = width
        self.height = height
        self.tiles = numpy.full((width, height), fill_value=tiletype.wall, order="F")
        self.visible = numpy.full((width, height), fill_value=False, order="F")
        self.explored = numpy.full((width, height), fill_value=False, order="F")
        self.entities = set(entities)

    def get_blocking_entity_at(self, x, y):
        def cond(entity):
            return entity.blocks_movement and entity.x == x and entity.y == y
        return next(filter(cond, self.entities), None)

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console):
        console.tiles_rgb[0:self.width, 0:self.height] = numpy.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tiletype.UNEXPLORED
        )

        entities_sorted_for_rendering = sorted(
            self.entities, key=lambda e: e.z
        )

        for entity in entities_sorted_for_rendering:
            if self.visible[entity.x, entity.y]:
                console.print(x=entity.x, y=entity.y, string=entity.char, fg=entity.color)

    def update_fov(self, x, y):
        self.visible[:] = tcod.map.compute_fov(
            self.tiles["transparent"],
            (x, y),
            radius=8
        )
        self.explored |= self.visible

    def get_path_to(self, acting_entity, dest_x, dest_y):
        """Compute and return a path to the target position.

        If there is no valid path then returns an empty list.
        """
        # Copy the walkable array.
        cost = numpy.array(self.tiles["walkable"], dtype=numpy.int8)

        for entity in self.entities:
            # Check that an entity blocks movement and the cost isn't zero (blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                # Add to the cost of a blocked position.
                # A lower number means more enemies will crowd behind each other in
                # hallways.  A higher number means enemies will take longer paths in
                # order to surround the player.
                cost[entity.x, entity.y] += 10

        # Create a graph from the cost array and pass that graph to a new pathfinder.
        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((acting_entity.x, acting_entity.y))  # Start position.

        # Compute the path to the destination and remove the starting point.
        path = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        # Convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]
