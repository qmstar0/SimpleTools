"""更改图片文件格式"""
from typing import Literal
import os
from PIL import Image

# #JPG -> PNG
# img_pil = Image.open('test.jpg')
# img_pil.convert('RGB').save('test.png', 'png')

# #PNG -> JPG
# img_pil = Image.open('test.png')
# img_pil.convert('RGB').save('test.jpg', 'jpeg')

# #JPG -> Webp
# img_pil = Image.open('test.jpg')
# img_pil.convert('RGB').save('test.webp', 'webp')
# #img_pil.save('test.webp', 'webp', optimize = True, quality = 10)

# #Webp -> JPG
# img_pil = Image.open('test.webp')
# img_pil.convert('RGB').save('test.jpg', 'jpeg')

# #PNG -> Webp
# img_pil = Image.open('test.png')
# img_pil.save('test.webp', 'webp')
# #img_pil.save('test.webp', 'webp', lossless = True)

# #Webp -> PNG
# img_pil = Image.open('test.webp')
# img_pil.save('test.png', 'png')

# img_pil = Image.open(r"D:\Python\AutoBILIBILI\tasks\task14\image.png")
# img_pil.convert('RGB').save(r'D:\Python\AutoBILIBILI\tasks\task14\image.jpg', 'jpeg')


class ChangeImageFormat:
    
    @staticmethod
    def is_image(filename: str):
        if filename.rsplit(".", 1)[-1] not in ["png", "jpg", "webp"]:
            return None
        return filename

    @staticmethod
    def filter(input_, filter_type):
        return filter(lambda x: x.split(".")[-1] == filter_type, input_)
    
    @staticmethod
    def image(img_path: str) -> Image.Image:
        return Image.open(img_path)

    @staticmethod
    def save(save_path: str, save_type: Literal["png", "jpeg", "webp"], img_obj: Image.Image) -> None:
        if save_type is not None:
            img_obj.convert('RGB').save(save_path, save_type)

    @staticmethod
    def _get_newfile_path(old_filename: str, save_type: str) -> str:
        if save_type == "jpeg":
            save_type = "jpg"
        return old_filename.rsplit(".", 1)[0] + f".{save_type}"

    @classmethod
    def change(cls, save_type: Literal["png", "jpeg", "webp"], input_path: str, out_path: str | None = None):
        img = cls.image(input_path)

        if out_path is not None:
            cls.save(out_path, save_type, img)
        cls.save(cls._get_newfile_path(input_path, save_type), save_type, img)
    
    @classmethod
    def task(cls, path: str, save_type: Literal["png", "jpeg", "webp"], *, only_choose: Literal["png", "jpeg", "webp", None] = None):
        assert not os.path.isfile(path), "方法错误 应该使用`ChangeImageFormat.change`"
        path_lis = [os.path.join(path, file) for file in os.listdir(path) if cls.is_image(file) is not None]

        if only_choose is not None:
            if only_choose == "jpeg":
                cls.filter(path_lis, "jpg")
            cls.filter(path_lis, only_choose)

        for file in path_lis:
            cls.change(save_type, file)

def change(save_type: Literal["png", "jpeg", "webp"], input_path: str, out_path: str | None = None):
    img = ChangeImageFormat.image(input_path)
    if out_path is not None:
        ChangeImageFormat.save(out_path, save_type, img)
    ChangeImageFormat.save(ChangeImageFormat._get_newfile_path(input_path, save_type), save_type, img)


if __name__ == '__main__':
    file = r"D:\MarkDown\blog\2022.11.22"
    # ChangeImageFormat.change("jpeg", file)
    ChangeImageFormat.task(file, 'webp', only_choose="png")
