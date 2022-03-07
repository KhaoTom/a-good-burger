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
            entity.move(self.delta_x, self.delta_y)
        else:
            entity.melee(target)
