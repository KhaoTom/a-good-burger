class Action:
    pass


class EscapeAction(Action):
    pass


class MovementAction(Action):
    def __init__(self, delta_x: int, delta_y: int):
        super().__init__()
        self.delta_x = delta_x
        self.delta_y = delta_y
