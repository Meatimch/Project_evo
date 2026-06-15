"""Statistic module.

Collects and exposes statistics about the simulation and populations.
"""


from dataclasses import dataclass


class Statistics:
    def __init__(self):
        self.population_size = 0
        self.sun_energy = 0
        self.mineral_energy = 0
        self.hunt_energy = 0
        self.height_distribution = []
        self.age_distribution = {}
        self.youngest_genome = []

    def collect(self, world):
        """Collects statistics from the current world state."""
        self.population_size = world.get_population()
        pass

    def collect_rare(self, world):
        self.height_distribution = [0] * world.size
        self.age_distribution = {}
        if len(world.bots) > 0:
            start_age = world.bots[0].age
            self.youngest_genome = world.bots[0].genome.genes
        for bot in world.bots:
            if bot.age < start_age:
                self.youngest_genome = bot.genome.genes
            self.height_distribution[bot.y] += 1
            self.age_distribution[bot.age] = self.age_distribution.get(bot.age, 0) + 1

    # ===================
    # ===== Сеттеры =====
    # ===================

    def set_sun_energy(self, ammount):
        self.sun_energy = ammount

    def set_mineral_energy(self, ammount):
        self.mineral_energy = ammount

    def set_hunt_energy(self, ammount):
        self.hunt_energy = ammount

    # ===================
    # ===== Геттеры =====
    # ===================

    def get_sun_energy(self):
        return self.sun_energy

    def get_mineral_energy(self):
        return self.mineral_energy

    def get_hunt_energy(self):
        return self.hunt_energy

    def nullify(self):
        """Resets all statistics to zero."""
        self.population_size = 0
        self.sun_energy = 0
        self.mineral_energy = 0
        self.hunt_energy = 0

@dataclass
class HistLogs:
    logs: list[str]