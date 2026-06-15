"""Bot module.

Contains the `Bot` class skeleton used by the simulation.

Note: no function implementations are provided — only basic structure.
"""

from genome import Genome
from world import World
from commands import *
import random


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
    _next_id = 1

    def __init__(self, genome: 'Genome', x=0, y=0, energy=100, is_multicell = False):
        self.genome = genome
        self.id = Bot._next_id
        Bot._next_id += 1
        self.energy = energy
        self.minerals = 0
        self.age = 0
        self.direction_index = 0
        self.x = x
        self.y = y
        self.is_multicell = is_multicell
        self.multicell_neighbors = set()
        # Сенсоры
        self.reg_energy = 0
        self.reg_minerals = 0
        self.reg_look = None
        self.reg_y = 0

    def execute_step(self, world: 'World', stats = None):
        self.stats = stats
        is_it_action = False
        counter = 0
        while not(is_it_action) and counter < 10:
            old_index = self.genome.current_index
            is_it_action = commands[self.genome.get_current_gene()](bot=self, world=world, stats = stats)
            if self.genome.current_index == old_index:
                self.genome.next_gene()
            counter+=1
        self.age += 1
        self.energy -= 1  # Базовая стоимость жизни
        if self.energy > 800:
            self.energy = 800
        if self.genome.current_index == old_index:
            self.genome.next_gene()
        return stats

    # ===================
    # ===== Геттеры =====
    # ===================

    def get_genome_index(self) -> int:
        """Returns the current index of the genome."""
        return self.genome.current_index
    
    def get_genome_gene(self) -> int:
        """Returns the current gene from the genome."""
        return self.genome.get_current_gene()
    
    def get_genes(self) -> list[int]:
        """Returns the list of genes in the genome."""
        return self.genome.genes

    def get_dx_dy(self):
        """Returns the current direction vector based on the bot's direction index."""
        return self.DIRECTIONS[self.direction_index]
    
    def get_look_at_cell(self, world: 'World'):
        """Returns the contents of the cell in front of the bot based on its current direction."""
        dx, dy = self.get_dx_dy()
        look_x = (self.x + dx) % world.size_x
        look_y = self.y + dy
        return world.get_cell(look_x, look_y)
    
    def get_look_direction(self, world: 'World') -> list: # лучше изменить на get_look_coordinates()
        dx, dy = self.get_dx_dy()
        look_x = (self.x + dx) % world.size_x
        look_y = self.y + dy
        return look_x, look_y
