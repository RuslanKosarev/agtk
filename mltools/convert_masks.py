# coding:utf-8
""" Training a face classifier.
"""

import click
from pathlib import Path
import numpy as np
import SimpleITK as sitk
import mltools


@click.command()
@click.option('-i', '--in_path', type=Path, required=True,
              help='Path for parsing.')
@click.option('-o', '--out_path', type=Path, default=None,
              help='Path for parsing.')
def main(in_path: Path, out_path: Path):
    in_path = in_path.expanduser()
    out_path = out_path.expanduser()

    dirs = np.unique([file.parent for file in in_path.rglob('*.dcm')])

    for dir_path in dirs:
        mltools.print_meta_data(dir_path)

        image = mltools.read_dicom_series(dir_path)
        print(dir_path, image.GetPixelIDTypeAsString())

        path = str(dir_path) + '.mha'
        if out_path:
            path = Path(path.replace(str(in_path), str(out_path)))
            mltools.mkdir(path.parent)

        nda = sitk.GetArrayFromImage(image)
        print(nda.min(), nda.max())

        threshold = sitk.BinaryThresholdImageFilter()
        threshold.SetLowerThreshold(-1024 + 1)
        threshold.SetUpperThreshold(32767)
        threshold.SetOutsideValue(0)
        threshold.SetInsideValue(1)
        image = threshold.Execute(image)

        nda = sitk.GetArrayFromImage(image)
        print(nda.min(), nda.max())

        sitk.WriteImage(image, str(path), useCompression=True)

    print(f'number of converted masks {len(dirs)}')


if __name__ == '__main__':
    main()
