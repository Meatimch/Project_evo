from statistics import HistLogs, Statistics

from bot import Bot
from genome import Genome
from world import World
import random


class Engine:
    def __init__(self, size=100, sun_income=100, mineral_income=100, mutation_rate=50):
        self.world = World(size=size, sun_income=sun_income, mineral_income=mineral_income)

        self.mutatuon_rate = mutation_rate
        self.tick = 0
        self.statistics = Statistics()
        self.hist_logs = HistLogs(logs=[])
        self.initialize_world()

    def step(self):
        self.statistics.nullify()
        logs = []
        self.tick += 1
        for bot in self.world.bots:
            if random.randint(0, 1000) < self.mutatuon_rate:
                bot.genome.mutate()
                logs.append(f"Tick {self.tick}: Bot {bot.id} at ({bot.x}, {bot.y}) mutated its genome to {bot.genome.genes}.")
            bot.execute_step(self.world, self.statistics)
            logs.append(f"Tick {self.tick}: Bot {bot.id} at ({bot.x}, {bot.y}) executed a step {bot.genome.get_current_gene()}.")
            self.hist_logs.logs.append(logs[-1])
        self.world.multicell_energy_flow()
        self.world.remove_dead()                      # Удаляем тех у кого энергия < 0
        self.world.bots.extend(self.world.new_bots)   # Добавляем в список ботов новорождённых
        self.world.new_bots.clear()                   # Удаляем список новорождённых
        self.statistics.collect(self.world)
        return self.statistics

    def initialize_world(self):
        #genome = Genome([0, 9, 2, 9, 4, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11, 0, 9, 2, 9, 4, 6, 9, 9, 9, 9, 9, 9, 9, 9, 9, 11])
        genome = Genome([9]*64)
        # genome.genes[10] = 0
        # genome.genes[11] = 11
        for i in range(0, self.world.size_x//2):
            for j in range(0, self.world.size // 3):
                bot = Bot(genome=genome.copy())
                bot.x = i * 2
                bot.y = self.world.size - 3 - j*2
                if bot.y >= self.world.size:
                    bot.y = self.world.size - 1
                self.world.bots.append(bot)
                self.world.set_cell(bot.x, bot.y, bot)
        print('world.bots len:', len(self.world.bots))
        print('grid[...]:', self.world.get_cell(bot.x, bot.y))
    pass

