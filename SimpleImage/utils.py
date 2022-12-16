"""更改图片文件格式"""

from typing import Literal
import os
from PIL import Image

IMG_TYPE = ("jpg", "webp", "png")


def _filter_image_file(path_: list[str]):

    return filter(
        lambda x: x.endswith(IMG_TYPE),
        path_
    )


def _change_and_save_(
    input_path: str,
    output_path: str,
    output_type: Literal["png", "jpg", "webp"],
) -> None:
    img = Image.open(input_path)
    img.convert('RGB').save(
        output_path, output_type if output_type != "jpg" else "jpeg")


def _batch_to_(
    input_path: list[str],
    output_type,
    output_path
):

    task_list = _filter_image_file(input_path)

    for path in task_list:
        output = os.path.join(
            output_path, f'{os.path.basename(path).rsplit(".")[0]}.{output_type}')

        _change_and_save_(
            input_path=path,
            output_path=output,
            output_type=output_type
        )


def to_jpg(
    input_path: str,
    save_path: str
):
    """转为 png

    Args:
        input_path (str): 输入路径
        save_path (str): 保存路径
    """
    _change_and_save_(
        input_path=input_path,
        output_path=save_path,
        output_type="jpg"
    )


def to_webp(
    input_path: str,
    save_path: str
):
    """转为 png

    Args:
        input_path (str): 输入路径
        save_path (str): 保存路径
    """
    _change_and_save_(
        input_path=input_path,
        output_path=save_path,
        output_type="webp"
    )


def to_png(
    input_path: str,
    save_path: str
):
    """转为 png

    Args:
        input_path (str): 输入路径
        save_path (str): 保存路径
    """
    _change_and_save_(
        input_path=input_path,
        output_path=save_path,
        output_type="png"
    )


def all_to_jpg(
    input_paths: list[str],
    output_path: str = "./"
):
    """全部转为 jpg

    Args:
        input_paths (list[str]): 文件路径的列表
        output_path (str, optional): 输出路径. 默认为 "./".
    """
    _batch_to_(
        input_path=input_paths,
        output_type="jpg",
        output_path=output_path
    )


def all_to_webp(
    input_paths: list[str],
    output_path: str = "./"
):
    """全部转为 webp

    Args:
        input_paths (list[str]): 文件路径的列表
        output_path (str, optional): 输出路径. 默认为 "./".
    """
    _batch_to_(
        input_path=input_paths,
        output_type="webp",
        output_path=output_path
    )


def all_to_png(
    input_paths: list[str],
    output_path: str = "./"
):
    """全部转为 png

    Args:
        input_paths (list[str]): 文件路径的列表
        output_path (str, optional): 输出路径. 默认为 "./".
    """
    _batch_to_(
        input_path=input_paths,
        output_type="png",
        output_path=output_path
    )


def folder_to_png(
    input_path: str,
    output_path: str | None = None
):
    """文件夹下图片 转为 png

    Args:
        input_path (str): 文件夹路径
        output_path (str | None, optional): 保存路径，为None时，与input_path相同.
    """
    assert os.path.isdir(input_path), "请传入一个文件夹路径"

    if output_path is None:
        output_path = input_path

    input_paths = [os.path.join(input_path, file)
                   for file in os.listdir(input_path)]

    _batch_to_(
        input_path=input_paths,
        output_type="png",
        output_path=output_path
    )


def folder_to_jpg(
    input_path: str,
    output_path: str | None = None
):
    """文件夹下图片 转为 jpg

    Args:
        input_path (str): 文件夹路径
        output_path (str | None, optional): 保存路径，为None时，与input_path相同.
    """
    assert os.path.isdir(input_path), "请传入一个文件夹路径"

    if output_path is None:
        output_path = input_path

    input_paths = [os.path.join(input_path, file)
                   for file in os.listdir(input_path)]

    _batch_to_(
        input_path=input_paths,
        output_type="jpg",
        output_path=output_path
    )


def folder_to_webp(
    input_path: str,
    output_path: str | None = None
):
    """文件夹下图片 转为 webp

    Args:
        input_path (str): 文件夹路径
        output_path (str | None, optional): 保存路径，为None时，与input_path相同.
    """
    assert os.path.isdir(input_path), "请传入一个文件夹路径"

    if output_path is None:
        output_path = input_path

    input_paths = [os.path.join(input_path, file)
                   for file in os.listdir(input_path)]

    _batch_to_(
        input_path=input_paths,
        output_type="webp",
        output_path=output_path
    )


# if __name__ == '__main__':
#     files = r"./"
#     folder_to_webp(files)
