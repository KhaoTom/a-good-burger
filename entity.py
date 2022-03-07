class Entity:
    def __init__(self, x: int, y: int, char: str, color: tuple[int, int, int]):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, delta_x: int, delta_y: int) -> None:
        self.x += delta_x
        self.y += delta_y
