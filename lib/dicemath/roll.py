import random


class Dice(object):
    def __init__(self, sides):
        self.sides = sides

    def __iter__(self):
        for i in range(1, self.sides + 1):
            yield i


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


def xdice(dice_list, input_sum=0):
    if len(dice_list) == 1:
        for n in dice_list[0]:
            yield input_sum + n
    else:
        pass_down_dice_list = dice_list[1:]
        for n in dice_list[0]:
            yield from xdice(pass_down_dice_list, input_sum=input_sum + n)


def xdice2(dice_list, rule_func, prev_rolls=None):
    if prev_rolls is None:
        pr = []
    else:
        pr = prev_rolls[:]
    if len(dice_list) == 1:
        for n in dice_list[0]:
            yield rule_func(pr, n)
    else:
        pass_down_dice_list = dice_list[1:]
        for n in dice_list[0]:
            yield from xdice2(pass_down_dice_list, rule_func, prev_rolls=pr + [n])


def advantage_gen():
    yield from xdice2([Dice(20)]*2, lambda x, y: max(x + [y]))


def disadvantage_gen():
    yield from xdice2([Dice(20)]*2, lambda x, y: min(x + [y]))


def _frequency(gen_func):
    f = {}
    for x in gen_func():
        try:
            f[x] += 1
        except KeyError:
            f[x] = 1
    return f


def advantage_frequency():
    return _frequency(advantage_gen)


def disadvantage_frequency():
    return _frequency(disadvantage_gen)


def _beat_tgt_frequency(gen_func):
    f = {}
    tgt_range = range(min(gen_func()), max(gen_func()) + 1)
    for r in gen_func():
        for tgt in tgt_range:
            if r >= tgt:
                try:
                    f[tgt] += 1
                except KeyError:
                    f[tgt] = 1
    return f


def advantage_beat_tgt_frequency():
    return _beat_tgt_frequency(advantage_gen)


def disadvantage_beat_tgt_frequency():
    return _beat_tgt_frequency(disadvantage_gen)


def xdicefrequency(dice_list):
    f = {}
    for x in xdice(dice_list):
        try:
            f[x] += 1
        except KeyError:
            f[x] = 1
    return f


def percentage_from_prob_dict(num, prob_dict):
    total = 0
    for k, v in prob_dict.items():
        total += v
    return (float(prob_dict[num]) / float(total)) * 100


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
