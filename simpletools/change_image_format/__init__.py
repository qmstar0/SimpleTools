
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


# def input_type_check(file_path: str, is_type) -> bool:
#     return file_path.endswith(f".{is_type}")


# def output_type_check(file_path: str, is_type) -> bool:
#     return file_path.endswith(f".{is_type}")


from .utils import folder_to_png, folder_to_jpg, folder_to_webp
from .utils import all_to_jpg, all_to_png, all_to_webp
from .utils import to_jpg, to_png, to_webp

