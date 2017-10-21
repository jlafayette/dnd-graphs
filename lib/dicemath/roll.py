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


def calculate_average(func, msg, num_turns=100000):
    total = 0
    for i in range(0, num_turns):
        total += func()
    average = float(total)/float(num_turns)
    print("{:>14}: {}".format(msg, average))


def print_averages():
    calculate_average(d6x2, "d6 x2")
    calculate_average(d6x2_drop_below3, "d6 x2 drop 1&2")
    calculate_average(d12, "d12")
    calculate_average(d12_drop_below3, "d12 drop 1&2")
