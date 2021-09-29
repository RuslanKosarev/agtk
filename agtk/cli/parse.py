# -*- coding: utf-8 -*-
""" Read and print meta data.
"""

import click
from pathlib import Path
import numpy as np

from agtk import dataset


@click.command()
@click.option('-p', '--path', type=Path, required=True,
              help='Path to directory to parse.')
def parse(path: Path):

    in_path = path.expanduser()
    dirs = list(in_path.glob('*'))

    paths = list(in_path.rglob('*'))
    paths.sort()

    for path in paths:
        if path in dirs:
            print()
        print(path)


if __name__ == '__main__':
    parse()
