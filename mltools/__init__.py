# coding:utf-8

from pathlib import Path
import pydicom as dicom
import SimpleITK as sitk


def mkdir(dir_path: Path):
    if not dir_path.parent.exists():
        dir_path.parent.mkdir(parents=True, exist_ok=True)


def read_meta_data(path: Path, *args, **kwargs):
    """

    :param path:
    :return:
    """

    if path.is_dir():
        path = list(path.rglob('*.dcm'))
        path.sort()
        path = path[0]

    items = dicom.dcmread(path, stop_before_pixels=True, *args, **kwargs)

    return items


def print_meta_data(path: Path):
    """

    :param path:
    """

    print(read_meta_data(path))


def read_dicom_series(path: Path):
    """

    :param path:
    :return:
    """
    reader = sitk.ImageSeriesReader()
    dicom_files = reader.GetGDCMSeriesFileNames(str(path))
    reader.SetFileNames(dicom_files)
    image = reader.Execute()

    return image
