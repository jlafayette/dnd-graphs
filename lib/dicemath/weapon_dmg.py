import plotly.plotly as py
import plotly.graph_objs as go

from . import roll, randomroll, utils

OUT_FOLDER_NAME = "weapon_dmg"
DICE = [
    {
        "random": randomroll.d6x2,
        "frequency": roll.frequency(roll.d6x2_gen),
        "label": "d6x2",
        "color": "#99a9b6",
        "mode": "lines",
        "yaxis": "y2"
    },
    {
        "random": randomroll.d6x2_drop_below3,
        "frequency": roll.frequency(roll.d6x2_reroll_below3_gen),
        "label": "d6x2 drop 1&2",
        "color": "#016bb4",
        "mode": "lines",
        "yaxis": "y2"
    },
    {
        "random": randomroll.d12,
        "frequency": roll.frequency(roll.d12_gen),
        "label": "d12",
        "color": "#ff9138",
        "mode": "lines"
    },
    {
        "random": randomroll.d12_drop_below3,
        "frequency": roll.frequency(roll.d12_reroll_below3_gen),
        "label": "d12 drop 1&2",
        "color": "#a70000",
        "mode": "lines"
    }
]


def get_frequency_trace(dice):
    frequency = dice['frequency']
    x = []
    y = []
    for i in range(min(frequency.keys()), max(frequency.keys())+1):
        x.append(i)
        try:
            # y.append(frequency[i])
            y.append(roll.percentage_from_prob_dict(i, frequency))
        except KeyError:
            y.append(0)
    return go.Scatter(x=x, y=y, mode=dice['mode'], name=dice['label'])


def get_value_over_turns_trace(dice, number_of_turns):
    x = []
    y = []
    for i in range(1, number_of_turns+1):
        x.append(i)
        y.append(dice['random']())
    return go.Scatter(x=x,
                      y=y,
                      mode=dice['mode'],
                      name=dice['label'],
                      line=go.Line(color=dice['color']),
                      xaxis=dice.get("xaxis", "x"),
                      yaxis=dice.get("yaxis", "y"))


def graph_frequency():
    data = []
    for dice in DICE:
        data.append(get_frequency_trace(dice))
    layout = go.Layout(title="Weapon Damage", width=800, height=640,
                       xaxis=dict(
                           nticks=12,
                           range=[1, 12],
                           title="Amount"
                       ),
                       yaxis=dict(
                           ticksuffix="%",
                           title="Frequency"
                       ))
    py.image.save_as(go.Figure(data=data, layout=layout),
                     filename=utils.file_from_name(OUT_FOLDER_NAME, "weapon-dmg-frequency"))


def graph_value_over_turns(num_turns):
    data = []
    for dice in DICE:
        data.append(get_value_over_turns_trace(dice, num_turns))
    layout = go.Layout(title="Value Over Turns", width=1200, height=640,
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
                     filename=utils.file_from_name(OUT_FOLDER_NAME,
                                                   "value-over-turns-{}".format(num_turns)))
