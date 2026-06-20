import math
from organic import Organic

class World:
    def __init__(self, size=100, sun_income=100, mineral_income=100):
        self.bots = []
        self.new_bots = []
        self.organics = {}
        self.size = size
        self.sun_income = sun_income
        self.mineral_income = mineral_income
        self.size_x = 150
        self.step = 0
        self.grid = [
            [None for _ in range(self.size_x)] 
            for _ in range(self.size)
        ]

    def get_population(self):
        """Returns the list of bots currently in the world."""
        return len(self.bots)

    def get_cell(self, x: int, y: int):
        """Returns the contents of the cell at (x, y)."""
        if 0 <= x < self.size_x and 0 <= y < self.size:
            return self.grid[y][x]
        return None  # Out of bounds
    
    def set_cell(self, x: int, y: int, object):
        """Sets the contents of the cell at (x, y) to object."""
        if 0 <= x < self.size_x and 0 <= y < self.size:
            self.grid[y][x] = object

    def is_cell_empty(self, x, y):
        if not (0 <= x < self.size_x and 0 <= y < self.size):
            return False
        if self.grid[y][x] is not None:
            return False
        return (x, y) not in self.organics
    
    def move_bot(self, bot, new_x: int, new_y: int):
        """Moves a bot to a new position if the cell is empty."""
        if self.is_cell_empty(new_x, new_y):
            self.set_cell(bot.x, bot.y, None)  # Clear old position
            self.set_cell(new_x, new_y, bot)  # Set new position
            bot.x, bot.y = new_x, new_y

    def connect_multicells(self, bot1, bot2):
            bot1.multicell_neighbors.add(bot2)
            bot2.multicell_neighbors.add(bot1)

            bot1.is_multicell = True
            bot2.is_multicell = True

    def remove_dead(self):
        new_bots = []
        for bot in self.bots:
            if bot.energy < 0:
                self.set_cell(bot.x, bot.y, None)
                for neighbor in bot.multicell_neighbors:
                    neighbor.multicell_neighbors.discard(bot)
                    if len(neighbor.multicell_neighbors) == 0:
                        neighbor.is_multicell = False
                bot.multicell_neighbors.clear()
                if bot.convert_to_organic == True and bot.hunted == False:
                    N = 100 + (bot.minerals * 2)
                    self.organics[(bot.x, bot.y)] = Organic(bot.x, bot.y, N)
            elif bot.energy >= 0:
                new_bots.append(bot)
        self.bots = new_bots.copy()

    def reproduce_bot(self, genome, x, y, energy, is_multicell=False, chain = [], obj=None):
        new_x, new_y, new_energy = x, y, energy
        new_genome = genome
        from bot import Bot
        if not(is_multicell):
            new_bot = Bot(
                genome = new_genome, 
                x = new_x, 
                y = new_y, 
                energy = new_energy)
            new_bot.genome.next_gene()
            self.new_bots.append(new_bot)
            self.set_cell(new_x, new_y, new_bot)
        new_chain=[]
        if is_multicell:
            new_bot = Bot(
                genome=new_genome,
                x=new_x,
                y=new_y,
                energy=new_energy,
                is_multicell=True
            )
            self.connect_multicells(obj, new_bot)
            self.new_bots.append(new_bot)
            self.set_cell(new_x, new_y, new_bot)
    pass

    def multicell_energy_flow(self):
        processed = set()
        for bot in self.bots:
            for neighbor in bot.multicell_neighbors:
                pair = tuple(sorted((bot.id,neighbor.id)))
                if pair in processed:
                    continue
                processed.add(pair)
                difference = (bot.energy -neighbor.energy)
                transfer = difference // 8
                if transfer > 0:
                    bot.energy -= transfer
                    neighbor.energy += transfer
                elif transfer < 0:
                    transfer = abs(transfer)
                    neighbor.energy -= transfer
                    bot.energy += transfer

    def remove_organic(self, x, y):
        if (x, y) in self.organics:
            del self.organics[(x, y)]
    
    def get_sun_boundary(self):
        YEAR_LENGTH = 10000             #Длина года в тиках
        
        summer_boundary = self.size // 3
        winter_boundary = self.size // 2
        
        time_fraction = (self.step % YEAR_LENGTH) / YEAR_LENGTH
        phase = (math.cos(time_fraction * 2 * math.pi) * -1 + 1) / 2
        
        current_boundary = summer_boundary + (winter_boundary - summer_boundary) * phase
        
        return int(current_boundary)

    def is_surrounded(self, x, y):
        """
        Проверяет, окружена ли клетка (x, y) со всех 8 сторон.
        Возвращает True, если свободных клеток нет.
        """
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx = (x + dx) % self.size_x
                ny = y + dy
                if ny < 0 or ny >= self.size:
                    continue
                if self.is_cell_empty(nx, ny):
                    return False
        return True
