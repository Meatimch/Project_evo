from statistics import HistLogs, Statistics

from bot import Bot
from genome import Genome
from world import World
import random


class Engine:
    def __init__(self, size=100, sun_income=100, mineral_income=100):
        self.world = World(size=size, sun_income=sun_income, mineral_income=mineral_income)

        self.tick = 0
        self.statistics = Statistics()
        self.hist_logs = HistLogs(logs=[])
        self.initialize_world()

    def step(self):
        self.statistics.nullify()
        logs = []
        self.tick += 1
        for bot in self.world.bots:
            stats = self.statistics
            _ = random.randint(0, 100)
            if _ < 15:
                bot.genome.mutate()
                logs.append(f"Tick {self.tick}: Bot {bot.id} at ({bot.x}, {bot.y}) mutated its genome to {bot.genome.genes}.")
            self.statistics = bot.execute_step(self.world, stats)
            logs.append(f"Tick {self.tick}: Bot {bot.id} at ({bot.x}, {bot.y}) executed a step {bot.genome.get_current_gene()}.")
            self.hist_logs.logs.append(logs[-1])
            pass
        self.world.remove_dead()                      # Удаляем тех у кого энергия < 0
        self.world.bots.extend(self.world.new_bots)   # Добавляем в список ботов новорождённых
        self.world.new_bots.clear()                   # Удаляем список новорождённых
        self.statistics.collect(self.world)
        return self.statistics

    def initialize_world(self):
        genome = Genome([0, 9, 2, 9, 4, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11])
        bot = Bot(genome=genome)
        bot.x = self.world.size // 2
        bot.y = self.world.size - 3
        self.world.bots.append(bot)
        self.world.set_cell(bot.x, bot.y, bot)
        print('world.bots len:', len(self.world.bots))
        print('grid[...]:', self.world.get_cell(bot.x, bot.y))
    pass

