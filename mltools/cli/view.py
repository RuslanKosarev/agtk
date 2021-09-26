# -*- coding: utf-8 -*-
""" Convert dicom series into 3D images.
"""

import click
from tqdm import tqdm
from pathlib import Path
import numpy as np
import SimpleITK as sitk
import mltools

from mltools.config import default_extension


@click.command()
@click.option('-p', '--path', type=Path, required=True,
              help='path to file or directory to print meta data.')
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
        image = mltools.read_meta_data(path)

        print('=================================================')
        print(path)
        print(image)


if __name__ == '__main__':
    view()
