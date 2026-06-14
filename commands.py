import random

from genome import Genome

def rotate_right(bot, world, stats):
    bot.direction_index = (bot.direction_index + 1) % 8
    return stats

def rotate_left(bot, world, stats):
    bot.direction_index = (bot.direction_index - 1) % 8
    return stats

def move_forward(bot, world, stats):
    dx, dy = bot.DIRECTIONS[bot.direction_index]
    if world.get_cell(bot.x + dx, bot.y + dy) == None and 0 <= bot.x+dx < world.size and 0 < bot.y+dy < world.size: # Проверяем, что впереди пусто
        world.move_bot(bot, bot.x + dx, bot.y + dy)
    else:
        bot.genome.next_gene()
    return stats

def move_backward(bot, world, stats):
    dx, dy = bot.DIRECTIONS[bot.direction_index]
    if world.get_cell(bot.x - dx, bot.y - dy) == None and 0 <= bot.x+dx < world.size and 0 < bot.y+dy < world.size: # Проверяем, что позади пусто
        world.move_bot(bot, bot.x - dx, bot.y - dy)
    else:
        bot.genome.next_gene()
    return stats

def how_many_minerals(bot, world, stats):
    bot.reg_minerals = bot.minerals
    return stats

def minerals_to_energy(bot, world, stats):
    if bot.reg_minerals > 0:
        energy_gained = bot.minerals * 1 - 10 # Конвертация с некоторыми потерями
        bot.energy += energy_gained
        bot.genome.jump(bot.genome.current_index + 1)
        bot.minerals = 0
    else:
        bot.genome.next_gene()
    return stats

def how_many_energy(bot, world, stats):
    bot.reg_energy = bot.energy
    return stats

def my_height(bot, world, stats):
    bot.reg_y = bot.y
    return stats

def look_around(bot, world, stats):
    bot.reg_look = bot.get_look_at_cell(world)
    return stats

def photosynthesize(bot, world, stats):
    const_sun = world.sun_income - (world.size - bot.y) * 5
    if const_sun > 0:
        bot.energy += const_sun
        stats.set_sun_energy(stats.get_sun_energy() + const_sun)
    else:
        bot.genome.next_gene()
    return stats
    
def get_minerals(bot, world, stats):
    const_minerals = world.mineral_income - bot.y * 5
    if const_minerals > 0:
        bot.minerals += const_minerals
        stats.set_mineral_energy(stats.get_mineral_energy() + const_minerals)
    else:
        bot.genome.jump(bot.genome.current_index + 1)
    return stats
    
def divide(bot, world, stats):
    look = bot.get_look_at_cell(world)
    x, y = bot.get_look_direction()
    if look == None and 0 <= x < world.size and 0 < y < world.size: # Если перед ботом пусто, то можно делиться
        if bot.reg_energy > 150: #знает ли бот, что у него достаточно энергии для деления
            if bot.energy > 150: # Условие для деления
                from bot import Bot
                bot.energy //= 2 # Делим энергию между родителем и потомком
                child_genome = bot.genome.copy()
                _ = random.randint(0, 100)
                if _ < 5: # 5% шанс на мутацию
                    child_genome.mutate()
                child_x, child_y = bot.get_look_direction()
                world.reproduce_bot(genome=child_genome, x=child_x, y=child_y, energy=bot.energy)
                bot.genome.next_gene()
            else:
                bot.genome.jump(bot.genome.current_index + 1)
        else:
            bot.genome.jump(bot.genome.current_index + 1)
    else:
        bot.genome.jump(bot.genome.current_index + 1)
    return stats

def hunt(bot, world, stats):
    look = bot.reg_look
    from bot import Bot
    if isinstance(look, Bot) and look.energy < bot.energy: # Если перед ботом другой бот с меньшей энергией, то можно охотиться
        bot.energy += look.energy // 2 # Получаем половину энергии жертвы
        look.energy = -999 # Жертва умирает
        bot.genome.next_gene()
        if stats.get_hunt_energy() + bot.energy > 0:
            stats.set_hunt_energy(stats.get_hunt_energy() + bot.energy)
    else:
        if bot.genome.current_index % 2 == 0:
            bot.genome.next_gene()
        else:
            bot.genome.jump(bot.genome.current_index + 1)
    return stats

commands = {
    0: rotate_right,
    1: rotate_left,
    2: move_forward,
    3: move_backward,
    4: how_many_minerals,
    5: minerals_to_energy,
    6: how_many_energy,
    7: my_height, # высота относительно дна
    8: look_around, # возвращает массив из 8 чисел - что находится вокруг бота
    9: photosynthesize,
    10: get_minerals,
    11: divide,
    12: hunt
}