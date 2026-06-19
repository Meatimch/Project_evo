import random

from genome import Genome

def rotate_right(bot, world, stats):
    bot.direction_index = (bot.direction_index + 1) % 8
    return False

def rotate_left(bot, world, stats):
    bot.direction_index = (bot.direction_index - 1) % 8
    return False

def move_forward(bot, world, stats):
    dx, dy = bot.DIRECTIONS[bot.direction_index]
    new_x = (bot.x + dx) % world.size_x   # зацикливание по X
    new_y = bot.y + dy
    if 0 <= new_y < world.size:            # Y не зациклен, просто проверка
        if world.get_cell(new_x, new_y) is None and not(bot.is_multicell):
            world.move_bot(bot, new_x, new_y)
        else:
            bot.genome.next_gene()
    else:
        bot.genome.next_gene()
    return True

def move_backward(bot, world, stats):
    dx, dy = bot.DIRECTIONS[bot.direction_index]
    new_x = (bot.x - dx) % world.size_x   # зацикливание по X
    new_y = bot.y - dy
    if 0 <= new_y < world.size:
        if world.get_cell(new_x, new_y) is None and not(bot.is_multicell):
            world.move_bot(bot, new_x, new_y)
        else:
            bot.genome.next_gene()
    else:
        bot.genome.next_gene()
    return True

def how_many_minerals(bot, world, stats):
    bot.reg_minerals = bot.minerals
    if bot.minerals > 0:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def minerals_to_energy(bot, world, stats):
    if bot.minerals > 0:
        energy_gained = bot.minerals * 3
        bot.energy += energy_gained
        bot.genome.jump(bot.genome.get_gene_shift(1))
        bot.minerals = 0
        stats.set_mineral_energy(stats.get_mineral_energy() + energy_gained)
    else:
        bot.genome.next_gene()
    return True

def how_many_energy(bot, world, stats):
    bot.reg_energy = bot.energy
    if bot.energy > 150:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def my_height(bot, world, stats):
    bot.reg_y = bot.y
    if bot.y > world.size // 2:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def look_around(bot, world, stats):
    bot.reg_look = bot.get_look_at_cell(world)
    if not(bot.reg_look is None):
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def photosynthesize(bot, world, stats):
    sun_boundary = world.get_sun_boundary()
    if bot.y > sun_boundary:
        zone_height = world.size - sun_boundary
        bot_height_in_zone = bot.y - sun_boundary
        const_sun = int(world.sun_income * (bot_height_in_zone / zone_height))
        mineral_bonus = bot.minerals // 100
        total_income = const_sun * (1 + mineral_bonus)
        bot.energy += total_income
        stats.set_sun_energy(stats.get_sun_energy() + total_income)
    else:
        bot.genome.next_gene()
    return True
    
def get_minerals(bot, world, stats):
    pass
    const_minerals = world.mineral_income - bot.y * 2
    if const_minerals > world.mineral_income // 10:
        bot.minerals += const_minerals
        #stats.set_mineral_energy(stats.get_mineral_energy() + const_minerals)
    else:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    return True
    
def divide(bot, world, stats):
    look = bot.get_look_at_cell(world)
    x, y = bot.get_look_direction(world)
    if look is None and 0 <= y < world.size: # Если перед ботом пусто, то можно делиться
        if bot.energy > 150: # Условие для деления
            from bot import Bot
            bot.energy //= 2 # Делим энергию между родителем и потомком
            child_genome = bot.genome.copy()
            if random.randint(0, 100) < 25: # 25% шанс на мутацию
                child_genome.mutate()
            world.reproduce_bot(genome=child_genome, x=x, y=y, energy=bot.energy)
            bot.genome.next_gene()
        else:
            bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return True

def multicell_divide(bot, world, stats):
    look = bot.get_look_at_cell(world)
    x, y = bot.get_look_direction(world)
    if look is None and 0 <= y < world.size:
        if bot.energy > 150: # Условие для деления
            from bot import Bot
            bot.energy //= 2 # Делим энергию между родителем и потомком
            child_genome = bot.genome.copy()
            if random.randint(0, 100) < 25: # 25% шанс на мутацию
                child_genome.mutate()
            world.reproduce_bot(genome=child_genome, x=x, y=y, energy=bot.energy, is_multicell=True, obj=bot)
            bot.genome.next_gene()
        else:
            bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))


def hunt(bot, world, stats):
    look = bot.get_look_at_cell(world)
    from bot import Bot
    if isinstance(look, Bot):
        if look.minerals == 0:
            can_hunt = True
        else:
            DEFENSE_MULTIPLIER = 5 # 1 минерал = 5 дополнительной энергии при защите
            effective_defense = look.energy + (look.minerals * DEFENSE_MULTIPLIER)
            can_hunt = bot.energy >= effective_defense
        if can_hunt:
            gained_energy = look.energy // 2
            bot.energy += gained_energy
            bot.minerals += look.minerals // 2
            look.energy = -999
            bot.genome.next_gene()
            if gained_energy > 0:
                stats.set_hunt_energy(stats.get_hunt_energy() + gained_energy)
        else:
            bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        if bot.genome.current_index % 2 == 0:
            bot.genome.next_gene()
        else:
            bot.genome.jump(bot.genome.get_gene_shift(2))
    return True

def jump_by_minerals(bot, world, stats):
    if bot.reg_minerals > bot.get_genome_index()**2 % world.mineral_income:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def jump_by_energy(bot, world, stats):
    if bot.reg_energy > bot.get_genome_index()**2 % world.sun_income:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def jump_by_height(bot, world, stats):
    if bot.reg_y > bot.get_genome_index()**2 % world.size:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def jump_by_object(bot, world, stats):
    if not(bot.reg_look is None):
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def is_it_border(bot, world, stats):
    x, y = bot.get_look_direction(world)
    if y < 0 or world.size < y:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return False

def filler(bot, world, stats):
    bot.genome.next_gene()
    #bot.genome.jump(bot.genome.get_gene_shift(0))
    return False

def is_i_look_at_sibling(bot, world, stats):
    diff = 0
    if bot.reg_look is None:
        bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        for a, b in zip(bot.genome.genes, bot.reg_look.genome.genes):
            if a != b:
                diff += 1
                if diff > 1:
                    bot.genome.jump(bot.genome.get_gene_shift(2))
                bot.genome.jump(3)
    return False

def share_energy(bot, world, stats):
    obj = bot.get_look_at_cell(world)
    if obj is not None:
        difference = bot.energy - obj.energy
        if difference > 0:
            transfer = difference // 4
            bot.energy -= transfer
            obj.energy += transfer
            bot.genome.jump(2)
        else:
            bot.genome.jump(bot.genome.get_gene_shift(1))
    else:
        bot.genome.jump(bot.genome.get_gene_shift(2))
    return True

commands = {
    0: rotate_right,
    1: rotate_left,
    2: move_forward,
    3: move_backward,
    4: how_many_minerals,
    5: minerals_to_energy,
    6: how_many_energy,
    7: my_height, # высота относительно дна
    8: look_around, # возвращает объект - бот / None
    9: photosynthesize,
    10: filler,           #tut bil get_minerals
    11: divide,
    12: hunt,
    13: jump_by_minerals,
    14: jump_by_energy,
    15: jump_by_height,
    16: jump_by_object,
    17: is_it_border,
    18: is_i_look_at_sibling,
    19: share_energy,
    20: multicell_divide,
    21: filler,
    22: filler,
    23: filler,
    24: filler,
    25: filler,
    26: filler,
    27: filler,
    28: filler,
    29: filler,
    30: filler,
    31: filler,
    32: filler,
    33: filler,	
    34: filler,	
    35: filler,	
    36: filler,
    37: filler,
    38: filler,
    39: filler,
    40: filler,
    41: filler,
    42: filler,
    43: filler,
    44: filler,
    45: filler,
    46: filler,
    47: filler,
    48: filler,
    49: filler,
    50: filler,
    51: filler,
    52: filler,
    53: filler,
    54: filler,
    55: filler,
    56: filler,
    57: filler,
    58: filler,
    59: filler,
    60: filler,
    61: filler,
    62: filler,
    63: filler
    }