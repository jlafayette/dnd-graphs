import sys
import pathlib

import click

_lib = pathlib.Path(__file__).parents[1].joinpath("lib")
if _lib not in sys.path:
    sys.path.insert(0, str(_lib))
from dicemath import advantage


@click.command()
def graph_advantage():
    advantage.graph_frequency()
    advantage.graph_beat_tgt_frequency()
    advantage.graph_pie()
    advantage.graph_value_over_turns(500)


if __name__ == '__main__':
    graph_advantage()
