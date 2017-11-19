import functools
import operator


class Dice(object):
    def __init__(self, sides):
        self.sides = sides

    def __iter__(self):
        for i in range(1, self.sides + 1):
            yield i


def d6_gen():
    yield from xdice([Dice(6)])


def d6x2_gen():
    yield from xdice([Dice(6)]*2)


def pairwise(iterable):
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    a = iter(iterable)
    return zip(a, a)


def _reroll_below_gen(dice_list, num):
    def func(prev_rolls, current_roll):
        result = 0
        for r1, r2 in pairwise(prev_rolls + [current_roll]):
            if r1 < num:
                result += r2
            else:
                result += r1
        # print("{} ==> {}".format(prev_rolls + [current_roll], result))
        return result
    expanded_list = []
    for dice in dice_list:
        expanded_list.extend([dice]*2)
    yield from xdice2(expanded_list, func)


def d6x2_reroll_below3_gen():
    yield from _reroll_below_gen([Dice(6)]*2, 3)


def d12_gen():
    yield from xdice([Dice(12)])


def d12_reroll_below3_gen():
    yield from _reroll_below_gen([Dice(12)], 3)


def d20_gen():
    yield from xdice([Dice(20)])


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


def frequency(gen_func):
    f = {}
    for x in gen_func():
        try:
            f[x] += 1
        except KeyError:
            f[x] = 1
    return f


def advantage_frequency():
    return frequency(advantage_gen)


def disadvantage_frequency():
    return frequency(disadvantage_gen)


def beat_tgt_frequency(gen_func):
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
    return beat_tgt_frequency(advantage_gen)


def disadvantage_beat_tgt_frequency():
    return beat_tgt_frequency(disadvantage_gen)


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


def average_from_gen(gen):
    combinations = len(list(gen()))
    total_sum = functools.reduce(operator.add, gen(), 0)
    return float(total_sum) / float(combinations)


def calculate_average(dice_list):
    def gen_func():
        yield from xdice(dice_list)
    return average_from_gen(gen_func)
