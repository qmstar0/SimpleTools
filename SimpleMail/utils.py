import os
import random

from email import encoders
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formataddr, parseaddr


def get_filedata(file_path: str) -> bytes:
    """获取文件数据

    Args:
        file_path (str): 文件路径

    Returns:
        bytes: 文件数据
    """
    with open(file_path, 'rb') as f:
        return f.read()


def get_filename(file_path: str) -> str:
    """获取文件名

    Args:
        file_path (str): 文件路径

    Returns:
        str: 文件名
    """
    return os.path.basename(file_path)


def encode_base64(obj: MIMEBase) -> MIMEBase:
    """对 obj 进行base64编码

    Args:
        obj (MIMEBase): MIMEBase或其子类
    """
    encoders.encode_base64(obj)
    return obj


def gener_random() -> str:
    """生成随机四位数id

    Returns:
        str: "imgxxxx"
    """
    nmb = random.randint(10, 99)
    i = random.randint(0, 24)
    return "img" +\
        str(nmb) +\
        str('abcdefghijklmnopqrstuvwxyz'[i:i+1])


def create(body, name, auto_header=False):
    if isinstance(body, str):

        if name is None:
            name = get_filename(body)
        data = get_filedata(body)
    elif isinstance(body, bytes):
        if name is None:
            raise
        data = body
    else:
        raise

    obj = MIMEBase("application", "octet-stream")
    obj.set_payload(data)
    if auto_header:
        obj.add_header('Content-Disposition', 'attachment', filename=name)
    encode_base64(obj)
    return obj


def addresse(mail: str, name: str | None = None) -> str:
    """格式化输出地址(发件人,收件人)

    Args:
        mail (str): 邮箱
        name (str | None, optional): 昵称，为None时使用邮箱号不带后缀.

    Returns:
        str: 格式化后的地址
    """
    if name is None:
        name, mail = parseaddr(mail)

    return formataddr((Header(name, "utf-8").encode(), mail))
