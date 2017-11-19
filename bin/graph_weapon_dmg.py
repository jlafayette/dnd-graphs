import sys
import pathlib

import click

_lib = pathlib.Path(__file__).parents[1].joinpath("lib")
if _lib not in sys.path:
    sys.path.insert(0, str(_lib))
from dicemath import weapon_dmg


@click.command()
def graph_weapon_dmg():
    weapon_dmg.graph_frequency()
    weapon_dmg.graph_value_over_turns(500)


if __name__ == '__main__':
    graph_weapon_dmg()
