"""Engine module.

Simulation engine skeleton responsible for advancing the world state.
"""

from statistics import HistLogs, Statistics

from bot import Bot
from genome import Genome
from world import World


class Engine:
    def __init__(self, size=100, sun_income=100, mineral_income=100):
        self.world = World(size=size, sun_income=sun_income, mineral_income=mineral_income)

        self.tick = 0
        self.statistics = Statistics()
        self.hist_logs = HistLogs(logs=[])
        self.initialize_world()

    def step(self):
        logs = []
        self.tick += 1
        for bot in self.world.bots:
            bot.execute_step(self.world)
            logs.append(f"Tick {self.tick}: Bot {bot.id} at ({bot.x}, {bot.y}) executed a step {bot.genome.get_current_gene()}.")
            self.hist_logs.logs.append(logs[-1])
            pass
        self.world.remove_dead()
        self.statistics.collect(self.world)
        return Statistics

    def initialize_world(self):
        genome = Genome([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        bot = Bot(genome=genome)
        self.world.bots.append(bot)
    pass

