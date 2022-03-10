class BoundedStat:
    """ Stat value with minimum and maximum bounds. """
    def __init__(self, minimum_value, maximum_value, start_value):
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.current_value = start_value

    def __repr__(self):
        return f"Stat({self.minimum_value}, {self.maximum_value}, {self.current_value})"

    def modify(self, amount):
        self.current_value = max(self.minimum_value, min(self.current_value + amount, self.maximum_value))

    def is_at_minimum(self):
        return self.current_value == self.minimum_value

    def is_at_maximum(self):
        return self.current_value == self.maximum_value