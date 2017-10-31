import math
import colorsys

import plotly.plotly as py
import plotly.graph_objs as go

from main import PROJ_PATH
import roll


def advantage():
    return max(roll.d20(), roll.d20())


def disadvantage():
    return min(roll.d20(), roll.d20())


DICE = [
    {
        "func": roll.d20,
        "label": "d20",
        "color": "#99a9b6",
        "mode": "lines",
    },
    {
        "func": advantage,
        "label": "Advantage",
        "color": "#99a9b6",
        "mode": "lines",
    },
    {
        "func": disadvantage,
        "label": "Disadvantage",
        "color": "#99a9b6",
        "mode": "lines",
    }
]


def get_frequency_trace(dice, num_turns=100000):
    frequency = roll.frequency(dice['func'], num_turns=num_turns)
    lo = min(frequency.keys())
    hi = max(frequency.keys())
    x = []
    y = []
    for i in range(lo, hi+1):
        x.append(i)
        try:
            y.append(float(frequency[i])/float(num_turns)*100)  # percentage
        except KeyError:
            y.append(0)
    return go.Scatter(x=x, y=y, mode=dice['mode'], name=dice['label'])


def graph_frequency(num_turns):
    data = []
    for dice in DICE:
        data.append(get_frequency_trace(dice, num_turns))

    hi = 5.0
    for d in data:
        hi = max(max(d['y']), hi)
    hi = math.ceil(hi)

    layout = go.Layout(title="Advantage vs Disadvantage", width=1200, height=640,
                       xaxis=dict(
                           nticks=20,
                           domain=[0, 1],
                           range=[1, 20],
                           title="Number on dice"
                       ),
                       yaxis=dict(
                           nticks=hi,
                           ticksuffix="%",
                           domain=[0, 1],
                           range=[0, hi]
                       ))
    py.image.save_as(go.Figure(data=data, layout=layout),
                     filename=_file_from_name("frequency"))


def get_beat_target_frequency(dice, num_turns=100000):
    frequency = roll.beat_target_frequency(dice['func'], range(1, 22), num_turns=num_turns)
    x = []
    y = []
    for i in range(1, 22):
        x.append(i)
        try:
            y.append(float(frequency[i])/float(num_turns)*100)  # percentage
        except KeyError:
            y.append(0)
    return go.Scatter(x=x, y=y, mode=dice['mode'], name=dice['label'])


def graph_beat_tgt_frequency(num_turns):
    data = []
    for dice in DICE:
        data.append(get_beat_target_frequency(dice, num_turns))

    layout = go.Layout(title="Advantage vs Targets", width=900, height=640,
                       xaxis=dict(
                           nticks=20,
                           domain=[0, 1],
                           range=[1, 21],
                           title="Target to beat"
                       ),
                       yaxis=dict(
                           nticks=20,
                           ticksuffix="%",
                           domain=[0, 1],
                           range=[0, 100]
                       ))
    py.image.save_as(go.Figure(data=data, layout=layout),
                     filename=_file_from_name("beat_tgt_frequency"))


def get_value_over_turns_trace(dice, number_of_turns):
    x = []
    y = []
    for i in range(1, number_of_turns+1):
        x.append(i)
        y.append(dice['func']())
    return go.Scatter(x=x,
                      y=y,
                      mode=dice['mode'],
                      name=dice['label'],
                      line=go.Line(color=dice['color'])
                      )


def graph_value_over_turns(name, num_turns):
    data = []
    for dice in DICE:
        data.append(get_value_over_turns_trace(dice, num_turns))
    layout = go.Layout(title=name, width=1200, height=640,
                       xaxis=dict(
                           nticks=10,
                           domain=[0, 1],
                           title="# of Damage Rolls"
                       ),
                       yaxis=dict(
                           nticks=12,
                           domain=[0, 0.45],
                           range=[1, 12],
                           title="d12"
                       ),
                       yaxis2=dict(
                           nticks=12,
                           domain=[0.55, 1],
                           range=[1, 12],
                           title="d6 x2"
                       ))
    py.image.save_as(go.Figure(data=data, layout=layout),
                     filename=_file_from_name(name))


def pie_trace(dice, num_turns):
    frequency = roll.frequency(dice['func'], num_turns=num_turns)
    labels = sorted(frequency.keys())
    values = []
    for label in labels:
        values.append(frequency[label])

    n = len(values)
    hsv_tuples = [(x * 1.0 / n, 0.5, 0.85) for x in range(n)]
    rgb_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples)
    print(rgb_tuples)
    colors = []
    for rgb in rgb_tuples:
        new_rgb = tuple([value*256 for value in rgb])
        colors.append("rgb{!s}".format(new_rgb))
        print(rgb)
    print(colors)

    print("values {}".format(values))
    print("label {}".format(labels))
    return go.Pie(values=values,
                  labels=labels,
                  text=labels,
                  sort=True,
                  name=dice['label'],
                  marker=dict(colors=colors)
                  )


def graph_pie(name, num_turns):
    data = [pie_trace(DICE[1], num_turns)]
    layout = go.Layout(title=name, width=640, height=640)
    py.image.save_as(go.Figure(data=data, layout=layout),
                     filename=_file_from_name("pie"))


def _file_from_name(name):
    file_ = PROJ_PATH.joinpath("out", "advantage")
    try:
        file_.mkdir()
    except FileExistsError:
        pass
    return file_.joinpath("{}.png".format(name))


def main():
    graph_frequency(1000000)
    graph_beat_tgt_frequency(100000)
    graph_pie("Advantage", 100000)


if __name__ == "__main__":
    main()
