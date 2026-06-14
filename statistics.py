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
        self.population_size = world.get_population()
    pass

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