# coding:utf-8

from typing import Union
from pathlib import Path
import pydicom as dicom
import SimpleITK as sitk

PathType = Union[str, Path]


def mkdir(dir_path: Path):
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)


class MetaData:
    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data

    def __str__(self):
        strings = [f'{key}:        {value}' for key, value in self._data.items()]

        return '\n'.join(strings)


def read_meta_data(path: PathType, default=None, *args, **kwargs):
    """

    :param path:
    :param default:
    :param args:
    :param kwargs:
    :return:
    """

    if path.is_dir():
        path = list(path.glob('*.dcm'))
        path.sort()
        path = path[0]

    if path.suffix == '.dcm':
        items = dicom.dcmread(path, stop_before_pixels=True, *args, **kwargs)
    else:
        try:
            reader = sitk.ImageFileReader()
            reader.SetFileName(str(path))
            reader.LoadPrivateTagsOn()
            reader.ReadImageInformation()

            items = {
                'pixel id': sitk.GetPixelIDValueAsString(reader.GetPixelID()),
                'dimension': reader.GetDimension(),
                'image size': reader.GetSize(),
                'number of components': reader.GetNumberOfComponents(),
                'pixel spacing': reader.GetSpacing(),
            }

            for key in reader.GetMetaDataKeys():
                items[key] = reader.GetMetaData(key)

            items = MetaData(items)

        except Exception as e:
            items = default

    return items


def print_meta_data(path: Path):
    """

    :param path:
    """

    print(read_meta_data(path))


def read_dicom_series(path: Path, meta_data_on: bool = True):
    """

    :param path:
    :param meta_data_on:
    :return:

    https://simpleitk.readthedocs.io/en/master/link_DicomSeriesReadModifyWrite_docs.html
    https://simpleitk.readthedocs.io/en/master/link_DicomImagePrintTags_docs.html
    """

    if not path.is_dir():
        raise IOError(f"ERROR: the directory '{path}' does not exist.")

    reader = sitk.ImageSeriesReader()

    dicom_files = reader.GetGDCMSeriesFileNames(str(path))
    if not dicom_files:
        raise IOError(f"ERROR: the directory '{path}' does not contain a DICOM series.")

    reader.SetFileNames(dicom_files)
    reader.MetaDataDictionaryArrayUpdateOn()
    reader.LoadPrivateTagsOn()
    image = reader.Execute()

    if meta_data_on:
        for key in reader.GetMetaDataKeys(0):
            image.SetMetaData(key, reader.GetMetaData(0, key))

    return image
