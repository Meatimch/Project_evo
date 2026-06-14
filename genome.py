import random

from commands import MAX_GENE_VALUE

"""Genome module.

Defines the `Genome` class skeleton which encapsulates genetic data for bots.
"""

class Genome:
    genes: list[int]
    current_index: int

    def __init__(self, genes):
        self.genes = genes
        self.current_index = 0

    def next_gene(self) -> int:
        """Сдвигает геном на 1"""
        gene = self.genes[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.genes) # Вместо +1 можно использовать более сложные формулы
        return gene

    def jump(self, offset: int) -> int:
        """Переходит к гену по смещению"""
        index = (self.current_index + offset) % len(self.genes)
        self.current_index = index
        return self.genes[index]
    
    def mutate(self):
        """Случайно изменяет один из генов"""
        index = random.randint(0, len(self.genes) - 1)
        self.genes[index] = random.randint(0, MAX_GENE_VALUE) # MAX_GENE_VALUE - максимальное значение для гена
        
    def copy(self) -> 'Genome':
        """Создает копию генома"""
        new_genome = Genome()
        new_genome.genes = self.genes
        new_genome.current_index = self.current_index # или можно 0 поставить
        return new_genome
    
    def get_current_gene(self) -> int:
        """Возвращает текущий ген без изменения индекса"""
        return self.genes[self.current_index]
    pass