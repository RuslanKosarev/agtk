# coding:utf-8
""" Training a face classifier.
"""

import click
import tqdm
from pathlib import Path
import numpy as np
import SimpleITK as sitk
import mltools


@click.command()
@click.option('-i', '--in_path', type=Path, required=True,
              help='input directory for parsing.')
@click.option('-o', '--out_path', type=Path, default=None,
              help='output directory to save results.')
def main(in_path: Path, out_path: Path):
    in_path = in_path.expanduser()
    out_path = out_path.expanduser()

    dirs = np.unique([file.parent for file in in_path.rglob('*.dcm')])

    for dir_path in tqdm(dirs):
        image = mltools.read_dicom_series(dir_path)

        path = str(dir_path) + '.mha'
        if out_path:
            path = Path(path.replace(str(in_path), str(out_path)))
            mltools.mkdir(path.parent)

        sitk.WriteImage(image, str(path), True)

    print(f'number of converted series {len(dirs)}')


if __name__ == '__main__':
    main()
