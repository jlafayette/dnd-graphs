import random


def roll(sides):
    return random.randint(1, sides)


def d6():
    return roll(6)


def d6x2():
    return d6() + d6()


def drop_below(func, num):
    r = func()
    if r < num:
        r = func()
    return r


def d6x2_drop_below3():
    return drop_below(d6, 3) + drop_below(d6, 3)


def d12():
    return roll(12)


def d12_drop_below3():
    return drop_below(d12, 3)


def d20():
    return roll(20)


def frequency(roll_func, num_turns=100000):
    frequency_dict = {}
    for i in range(0, num_turns):
        r = roll_func()
        try:
            frequency_dict[r] += 1
        except KeyError:
            frequency_dict[r] = 1
    return frequency_dict


def beat_target_frequency(roll_func, tgt_range, num_turns=100000):
    frequency_dict = {}
    for i in range(0, num_turns):
        r = roll_func()
        for tgt in tgt_range:
            if r >= tgt:
                try:
                    frequency_dict[tgt] += 1
                except KeyError:
                    frequency_dict[tgt] = 1
    return frequency_dict


def calculate_average(func, msg, num_turns=100000):
    total = 0
    for i in range(0, num_turns):
        total += func()
    average = float(total)/float(num_turns)
    print("{:>14}: {}".format(msg, average))
