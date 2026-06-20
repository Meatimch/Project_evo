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
        self.convert_to_organic = False
        self.hunted = False

    def execute_step(self, world: 'World', stats = None):
        self.stats = stats
        is_it_action = False
        counter = 0
        MINERAL_ZONE_LIMIT = 50
        gradient = 1.0 - (self.y / (MINERAL_ZONE_LIMIT + 1))
        if self.y <= MINERAL_ZONE_LIMIT:
            self.minerals += int(world.mineral_income * gradient)
            if self.minerals > 50:
                self.minerals = 50
        while not(is_it_action) and counter < 10:
            old_index = self.genome.current_index
            is_it_action = commands[self.genome.get_current_gene()](bot=self, world=world, stats = stats)
            if self.genome.current_index == old_index:
                self.genome.next_gene()
            counter+=1
        self.age += 1
        # if self.age > 10000 and random.randint(0, 1000) < 2:
        #     self.energy = -999
        self.energy -= 1  # Базовая стоимость жизни

        if self.energy > 1000:
            if world.is_surrounded(self.x, self.y):
                self.energy = -999
                self.convert_to_organic = True
            else:
                self.energy = 1000
                temporary_index = self.genome.current_index
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx = (self.x + dx) % world.size_x
                        ny = self.y + dy
                        if world.is_cell_empty(nx, ny):
                            self.direction_index = self.DIRECTIONS.index((dx, dy))
                            commands[20](bot=self, world=world, stats = stats)
                self.genome.current_index = temporary_index
        if self.energy <= 0:
            self.convert_to_organic = True

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
