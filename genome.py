import random
import os
MAX_GENE_VALUE = 63

class Genome:
    genes: list[int]
    current_index: int

    def __init__(self, genes):
        self.genes = genes
        self.current_index = 0

    def next_gene(self, shift = 1) -> int:
        """Сдвигает геном на 1"""
        gene = self.genes[self.current_index]
        self.current_index = (self.current_index + shift) % len(self.genes) # Вместо +1 можно использовать более сложные формулы
        return gene

    def jump(self, offset: int) -> int:
        """Переходит к гену по смещению"""
        index = (self.current_index + offset) % len(self.genes)
        self.current_index = index
        return self.genes[index]
    
    def mutate(self):
        """Случайно изменяет один из генов"""
        #random.seed(int.from_bytes(os.urandom(4), 'big'))
        index = random.randint(0, len(self.genes) - 1)
        self.genes[index] = random.randint(0, MAX_GENE_VALUE) # MAX_GENE_VALUE - максимальное значение для гена
        #self.current_index = random.randint(0, len(self.genes) - 1)
        
    def copy(self) -> 'Genome':
        """Создает копию генома"""
        new_genome = Genome(self.genes.copy())
        new_genome.current_index = self.current_index
        return new_genome
    
    def get_current_gene(self) -> int:
        """Возвращает текущий ген без изменения индекса"""
        return self.genes[self.current_index]
    
    def get_gene_shift(self, shift) -> int:
        """Возвращает ген cur_ind + shift без изменения индекса"""
        return self.genes[(self.current_index+shift)%MAX_GENE_VALUE]
