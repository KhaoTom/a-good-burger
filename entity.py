class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
