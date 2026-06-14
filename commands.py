MAX_GENE_VALUE = 9

def rotate_right(bot, world) -> None:
    bot.direction_index = (bot.direction_index + 1) % 8
    #print(f"Bot rotated right. New direction index: {bot.direction_index}")

def rotate_left(bot, world) -> None:
    bot.direction_index = (bot.direction_index - 1) % 8
    #print(f"Bot rotated left. New direction index: {bot.direction_index}")

def move_forward(bot, world) -> None:
    dx, dy = bot.DIRECTIONS[bot.direction_index]
    bot.x += dx
    bot.y += dy

def move_backward(bot, world) -> None:
    dx, dy = bot.DIRECTIONS[bot.direction_index]
    bot.x -= dx
    bot.y -= dy

def how_many_minerals(bot, world) -> int:
    # Заглушка, возвращает случайное число минералов
    return bot.minerals

def minerals_to_energy(bot, world) -> None:
    # Конвертирует минералы в энергию (пример: 1 минерал = 2 единицы энергии)
    energy_gained = bot.minerals * 2 - 10 # Конвертация с некоторыми потерями
    bot.energy += energy_gained
    bot.minerals = 0
    #print(f"Bot converted minerals to energy. Gained {energy_gained} energy, now has {bot.energy} energy.")

def how_many_energy(bot, world) -> int:
    return bot.energy

def my_height(bot, world) -> int:
    # Заглушка, возвращает высоту относительно дна (можно использовать координату y для простоты)
    return bot.y

def look_around(bot, world) -> list[int]:
    # Заглушка, возвращает массив из 8 чисел - что находится вокруг бота
    # Например: 0 - пусто, 1 - минералы, 2 - другой бот, 3 - солнце и т.д.
    return [0] * 8

def photosynthesize(bot, world) -> None:
    # Заглушка, увеличивает энергию бота на фиксированное количество (например, 5 единиц)
    if world.sun_income - bot.y * 5 > 0:
        bot.energy += (world.sun_income - bot.y * 5)
    else:
        pass

def get_minerals(bot, world) -> None:
    if world.mineral_income - (world.size - bot.y) * 5 > 0:
        bot.minerals += (world.mineral_income - (world.size - bot.y) * 5)
    else:
        pass
        
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
    10: get_minerals
}