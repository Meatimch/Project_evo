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

    def collect(self, world):
        """Collects statistics from the current world state."""
        self.population_size = len(world.bots)
        # Заглушки для энергии
        self.sun_energy = 0
        self.mineral_energy = 0
        self.hunt_energy = 0
    pass

@dataclass
class HistLogs:
    logs: list[str]