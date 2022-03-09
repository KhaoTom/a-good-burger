from game import *


class Action:
    def perform(self, engine, entity):
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine, entity):
        raise SystemExit()


class DirectionalAction(Action):
    def __init__(self, delta_x, delta_y):
        super().__init__()
        self.delta_x = delta_x
        self.delta_y = delta_y

    def perform(self, engine, entity):
        raise NotImplementedError()


class MovementAction(DirectionalAction):
    def perform(self, engine, entity):
        new_x = entity.x + self.delta_x
        new_y = entity.y + self.delta_y

        if not engine.game_map.in_bounds(new_x, new_y):
            return
        if not engine.game_map.tiles["walkable"][new_x, new_y]:
            return

        target = engine.game_map.get_blocking_entity_at(new_x, new_y)
        if target is None:
            move(entity, self.delta_x, self.delta_y)
        else:
            melee(entity, target)


class WaitAction(Action):
    def perform(self, engine, entity):
        pass


class HostileAction(Action):
    path = None

    def perform(self, engine, entity):
        target = engine.player
        dx = target.x - entity.x
        dy = target.y - entity.y
        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if engine.game_map.visible[entity.x, entity.y]:
            if distance <= 1:
                MovementAction(dx, dy).perform(engine, entity)
                return

            self.path = engine.game_map.get_path_to(entity, target.x, target.y)

        if self.path:
            dest_x, dest_y = self.path.pop(0)
            MovementAction(dest_x - entity.x, dest_y - entity.y).perform(engine, entity)
            return

        WaitAction().perform(engine, entity)
