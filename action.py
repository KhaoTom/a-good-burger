class Action:
    def perform(self, engine, entity):
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self, engine, entity):
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, delta_x: int, delta_y: int):
        super().__init__()
        self.delta_x = delta_x
        self.delta_y = delta_y

    def perform(self, engine, entity):
        new_x = entity.x + self.delta_x
        new_y = entity.y + self.delta_y

        if not engine.game_map.in_bounds(new_x, new_y):
            return
        if not engine.game_map.tiles["walkable"][entity.x + self.delta_x, entity.y + self.delta_y]:
            return

        entity.move(self.delta_x, self.delta_y)
