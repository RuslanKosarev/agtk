# -*- coding: utf-8 -*-
""" Read and print meta data.
"""

import click
from pathlib import Path
import numpy as np

from agtk import dataset


@click.command()
@click.option('-p', '--path', type=Path, required=True,
              help='Path to file or directory to print meta data.')
def view(path: Path):

    path = path.expanduser()

    if path.is_file():
        paths = [path]
    else:
        paths = []
        for path in path.rglob('*'):
            if path.is_file():
                paths.append(path.parent if '.dcm' == path.suffix else path)
        paths = np.unique(paths)

    for path in paths:
        data = dataset.read_meta_data(path)

        print('=================================================')
        print(path)
        print(data)


if __name__ == '__main__':
    view()
