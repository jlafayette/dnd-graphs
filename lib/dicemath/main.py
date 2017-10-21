import pathlib

import plotly.plotly as py
import plotly.graph_objs as go

import roll


PROJ_PATH = pathlib.Path(__file__).parents[2]


def get_frequency_trace(func, name, num=20):
    frequency = {}
    for i in range(0, num):
        r = func()
        try:
            frequency[r] += 1
        except KeyError:
            frequency[r] = 1
    x = []
    y = []
    for i in range(min(frequency.keys()), max(frequency.keys())+1):
        x.append(i)
        try:
            # y.append(float(frequency[i])/float(num))
            y.append(frequency[i])
        except KeyError:
            y.append(0)
    return go.Scatter(x=x, y=y, mode="lines+markers", name=name)


def get_value_over_turns_trace(dice, number_of_turns):
    x = []
    y = []
    for i in range(1, number_of_turns+1):
        x.append(i)
        y.append(dice['func']() + dice.get('offset', 0))
    return go.Scatter(x=x,
                      y=y,
                      mode=dice['mode'],
                      name=dice['label'],
                      line=go.Line(color=dice['color']))


def create_run(name, num):
    d6x2_trace = get_frequency_trace(roll.d6x2, "d6x2", num=num)
    d12_trace = get_frequency_trace(roll.d12, "d12", num=num)
    d6x2_drop12_trace = get_frequency_trace(roll.d6x2_drop_below3,
                                            "d6x2 drop 1&2", num=num)
    d12_drop12_trace = get_frequency_trace(roll.d12_drop_below3,
                                           "d12 drop 1&2", num=num)

    data = [d6x2_trace, d12_trace, d6x2_drop12_trace, d12_drop12_trace]
    layout = go.Layout(title=name, width=800, height=640)
    fig = go.Figure(data=data, layout=layout)
    outpath = os.path.join(PROJ_DIR, "out", "{}.png".format(name))
    py.image.save_as(fig, filename=outpath)


def create_series():
    num = 1000
    out_prefix = "line-plot-compare-{}".format(num)
    for i in range(1, 6):
        out_image = "{}-{}".format(out_prefix, i)
        create_run(out_image, num)


dice_data = [
    {
        "func": roll.d6x2,
        "label": "d6x2",
        "color": "#99a9b6",
        "mode": "lines",
        "offset": 12
    },
    {
        "func": roll.d6x2_drop_below3,
        "label": "d6x2 drop 1&2",
        "color": "#016bb4",
        "mode": "lines",
        "offset": 12
    },
    {
        "func": roll.d12,
        "label": "d12",
        "color": "#ff9138",
        "mode": "lines"
    },
    {
        "func": roll.d12_drop_below3,
        "label": "d12 drop 1&2",
        "color": "#a70000",
        "mode": "lines"
    }
]


def main():
    num_turns = 500
    name = "value-over-turns-{}-5".format(num_turns)
    data = []
    for dice in dice_data:
        data.append(get_value_over_turns_trace(dice, num_turns))
    layout = go.Layout(title=name, width=1200, height=640)
    fig = go.Figure(data=data, layout=layout)
    py.image.save_as(fig,
                     filename=PROJ_PATH.joinpath("out", "{}.png".format(name)))


if __name__ == "__main__":
    main()
