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
    image = reader.Execute()

    reader.MetaDataDictionaryArrayUpdateOn()
    reader.LoadPrivateTagsOn()

    for key in reader.GetMetaDataKeys(0):
        image.SetMetaData(key, reader.GetMetaData(0, key))

    return image
