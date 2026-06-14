"""World module.

Defines the `World` skeleton that contains the environment and grid state.
"""

class World:
    def __init__(self, size=100, sun_income=100, mineral_income=100):
        self.bots = []
        self.size = size
        self.sun_income = sun_income
        self.mineral_income = mineral_income
        self.grid = [
            [None for _ in range(self.size)] 
            for _ in range(self.size)
        ]

    def get_cell(self, x: int, y: int):
        """Returns the contents of the cell at (x, y)."""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.grid[y][x]
        return None  # Out of bounds
    
    def set_cell(self, x: int, y: int, object):
        """Sets the contents of the cell at (x, y) to object."""
        if 0 <= x < self.size and 0 <= y < self.size:
            self.grid[y][x] = object

    def is_cell_empty(self, x: int, y: int) -> bool:
        """Checks if the cell at (x, y) is empty."""
        return self.get_cell(x, y) is None
    
    def move_bot(self, bot, new_x: int, new_y: int):
        """Moves a bot to a new position if the cell is empty."""
        if self.is_cell_empty(new_x, new_y):
            self.set_cell(bot.x, bot.y, None)  # Clear old position
            bot.x = new_x
            bot.y = new_y
            self.set_cell(new_x, new_y, bot)  # Set new position

    def remove_dead(self):
        """Removes bots that have died (energy <= 0) from the world."""
        self.bots = [bot for bot in self.bots if bot.energy > 0]
    pass
