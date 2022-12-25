import random

from email.utils import formataddr, parseaddr
from email.header import Header

def gener_random() -> str:
    """生成随机四位数id

    Returns:
        str: "imgxxxx"
    """
    nmb = random.randint(10, 99)
    i = random.randint(0, 24)
    return "img" +\
        str(nmb) +\
        str('abcdefghijklmnopqrstuvwxyz'[i:i+2])

def address(mail: str, name: str | None = None) -> str:
    """格式化输出地址(发件人/收件人)

    Args:
        mail (str): 邮箱
        name (str | None, optional): 昵称， 可为None

    Returns:
        str: 格式化后的地址
    """
    if name is None:
        name, mail = parseaddr(mail)

    return formataddr((Header(name, "utf-8").encode(), mail))
