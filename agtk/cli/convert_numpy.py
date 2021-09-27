# -*- coding: utf-8 -*-
""" Convert dicom series into 3D images.
"""

import click
from tqdm import tqdm
from pathlib import Path
import numpy as np
import SimpleITK as sitk

from agtk.dataset.config import default_extension
from agtk import dataset


@click.command()
@click.option('-i', '--in_path', type=Path, required=True,
              help='Input directory for parsing.')
@click.option('-o', '--out_path', type=Path, default=None,
              help='Output directory to save images.')
@click.option('-e', '--ext', type=str, default=default_extension,
              help=f'Format to save images, {default_extension} is default.')
def convert_series(in_path: Path, out_path: Path, ext: str):

    in_path = in_path.expanduser()

    if out_path is None:
        out_path = Path(f'{in_path}3D{ext[1:]}')
    out_path = out_path.expanduser()

    dirs = np.unique([file.parent for file in in_path.rglob('*.npy')])

    for dir_path in dirs:
        image_path = Path(str(dir_path).replace('Masks', 'Images'))

        if image_path.exists():
            files = list(dir_path.glob('*.npy'))
            files.sort()
            slices = [np.load(file) for file in files]

            mask = np.stack(slices, axis=0)
            print(dir_path, f'[{np.min(mask)}, {np.max(mask)}]')
            mask = sitk.GetImageFromArray(mask)

            image = dataset.read_dicom_series(image_path)

            mask.CopyInformation(image)

            path = str(dir_path) + ext
            path = Path(path.replace(str(in_path), str(out_path)))
            dataset.mkdir(path.parent)

            sitk.WriteImage(mask, str(path), True)

    print(f'number of converted series {len(dirs)}')


if __name__ == '__main__':
    convert_series()
