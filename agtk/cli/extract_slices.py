# -*- coding: utf-8 -*-
""" Extract slices from 3D images.
"""

import click
from tqdm import tqdm
from pathlib import Path
from loguru import logger

import SimpleITK as sitk

from agtk import logging
from agtk import dataset


@click.command()
@click.option('-i', '--in_path', type=Path, required=True,
              help='Input directory for parsing.')
@click.option('-o', '--out_path', type=Path, required=True,
              help='Output directory to save images.')
def extract_slices(
        in_path: Path,
        out_path: Path,
):

    in_path = in_path.expanduser()
    out_path = out_path.expanduser()

    logging.configure_logging(out_path)
    logger.info('Input directory for parsing {in_path}.', in_path=in_path)
    logger.info("Output directory to save images {out_path}.", out_path=out_path)

    files = [file for file in in_path.rglob('*') if file.is_file()]
    count = 0

    for file in tqdm(files):
        try:
            image = sitk.ReadImage(str(file))
        except Exception:
            continue

        if image.GetDimension() == 3:
            count += 1

            path = Path(str(file.parent).replace(str(in_path), str(out_path))) / file.stem
            dataset.mkdir(path)

            for idx in range(image.GetDepth()):
                slice2d = image[:, :, idx]
                sitk.WriteImage(slice2d, str(path / f'{idx + 1:03d}{file.suffix}'), True)

    logger.info("Number of converted files {count}.", count=count)


if __name__ == '__main__':
    extract_slices()
