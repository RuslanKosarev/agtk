# -*- coding: utf-8 -*-
""" Convert dicom masks into 3D binary images.
"""

import click
from tqdm import tqdm
from pathlib import Path
from loguru import logger

import numpy as np
import SimpleITK as sitk

from agtk import logging
from agtk import dataset
from agtk.dataset.config import default_extension


@click.command()
@click.option('-i', '--in_path', type=Path, required=True,
              help='Input directory for parsing.')
@click.option('-o', '--out_path', type=Path, default=None,
              help='Output directory to save images.')
@click.option('-b', '--background', type=int, default=0,
              help='Background value for saved mask.')
@click.option('-f', '--foreground', type=int, default=1,
              help='Foreground value for saved mask.')
@click.option('-e', '--ext', type=str, default=default_extension,
              help=f'Format to save images, {default_extension} is default.')
def convert_masks(
        in_path: Path,
        out_path: Path,
        background: int,
        foreground: int,
        ext: str
    ):

    in_path = in_path.expanduser()

    if out_path is None:
        out_path = Path(f'{in_path}3D{ext[1:]}')
    out_path = out_path.expanduser()

    logging.configure_logging(out_path)
    logger.info('Input directory for parsing {in_path}.', in_path=in_path)

    lower_threshold = -1024 + 1
    upper_threshold = 32767

    dirs = np.unique([file.parent for file in in_path.rglob('*.dcm')])

    for dir_path in tqdm(dirs):
        image = dataset.read_dicom_series(dir_path)

        path = str(dir_path) + ext
        path = Path(path.replace(str(in_path), str(out_path)))
        dataset.mkdir(path.parent)

        threshold = sitk.BinaryThresholdImageFilter()
        threshold.SetLowerThreshold(lower_threshold)
        threshold.SetUpperThreshold(upper_threshold)
        threshold.SetOutsideValue(background)
        threshold.SetInsideValue(foreground)
        processed_image = threshold.Execute(image)

        for key in image.GetMetaDataKeys():
            processed_image.SetMetaData(key, image.GetMetaData(key))

        sitk.WriteImage(processed_image, str(path), True)

    logger.info("Directory with saved images {out_path}.", out_path=out_path)
    logger.info("Number of converted masks {num_dirs}.", num_dirs=len(dirs))


if __name__ == '__main__':
    convert_masks()
