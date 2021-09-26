# -*- coding: utf-8 -*-
""" Convert dicom masks into 3D binary images.
"""

import click
from tqdm import tqdm
from pathlib import Path
import numpy as np
import SimpleITK as sitk

from agtk.config import default_extension
from agtk import dataset


@click.command()
@click.option('-i', '--in_path', type=Path, required=True,
              help='input directory for parsing.')
@click.option('-o', '--out_path', type=Path, default=None,
              help='output directory to save results.')
@click.option('-e', '--ext', type=str, default=default_extension,
              help=f'format to save images, {default_extension} is default.')
def convert_masks(in_path: Path, out_path: Path, ext: str):

    in_path = in_path.expanduser()
    out_path = out_path.expanduser()

    lower_threshold = -1024 + 1
    upper_threshold = 32767

    outside_value = 0
    inside_value = 1

    dirs = np.unique([file.parent for file in in_path.rglob('*.dcm')])

    for dir_path in tqdm(dirs):
        image = dataset.read_dicom_series(dir_path)

        path = str(dir_path) + ext

        if out_path:
            path = Path(path.replace(str(in_path), str(out_path)))
            dataset.mkdir(path.parent)

        threshold = sitk.BinaryThresholdImageFilter()
        threshold.SetLowerThreshold(lower_threshold)
        threshold.SetUpperThreshold(upper_threshold)
        threshold.SetOutsideValue(outside_value)
        threshold.SetInsideValue(inside_value)
        processed_image = threshold.Execute(image)

        for key in image.GetMetaDataKeys():
            processed_image.SetMetaData(key, image.GetMetaData(key))

        sitk.WriteImage(processed_image, str(path), True)

    print(f'number of converted masks {len(dirs)}')


if __name__ == '__main__':
    convert_masks()
