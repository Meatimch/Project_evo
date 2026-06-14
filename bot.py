"""Bot module.

Contains the `Bot` class skeleton used by the simulation.

Note: no function implementations are provided — only basic structure.
"""

from genome import Genome
from world import World
from commands import *


class Bot:
    genome: 'Genome'
    id : int
    energy: int
    minerals: int
    age: int
    direction_index: int
    x: int
    y: int
    DIRECTIONS = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

    def __init__(self, genome: 'Genome'):
        self.genome = genome
        self.id = id(self)
        self.energy = 100
        self.minerals = 0
        self.age = 0
        self.direction_index = 0
        self.x = 0
        self.y = 0

    def execute_step(self, world: 'World'):
        commands[self.genome.get_current_gene()](bot=self, world=world)
        self.age += 1
        self.genome.current_index = (self.genome.current_index + 1) % len(self.genome.genes) # Сдвигаем геном на 1
        pass

    # ===================
    # ===== Геттеры =====
    # ===================

    def get_dx_dy(self):
        """Returns the current direction vector based on the bot's direction index."""
        return self.DIRECTIONS[self.direction_index]
    
    def get_look_at_cell(self, world: 'World'):
        """Returns the contents of the cell in front of the bot based on its current direction."""
        dx, dy = self.get_dx_dy()
        look_x = self.x + dx
        look_y = self.y + dy
        # Заглушка: возвращает 0 (пусто) для всех клеток
        return 0
    pass
