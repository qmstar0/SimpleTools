import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.encoders import encode_base64

from .exception import *
from .utils import gener_random


class MailContent:
    """邮件内容
    """

    def __init__(self) -> None:
        self.__box = MIMEMultipart('mixed')
        self.__msg = MIMEMultipart('related', type="multipart/alternative")
        self.__cnt = MIMEMultipart('alternative')
        self.__msg.attach(self.__cnt)
        self.__box.attach(self.__msg)

    @property
    def Subject(self):
        """主题, 不设置可能会导致邮件代发商误判为垃圾邮件"""
        return self.__box.get("Subject")

    @Subject.setter
    def Subject(self, other):
        """主题, 不设置可能会导致邮件代发商误判为垃圾邮件"""
        self.__check_str(other)
        self.__box["Subject"] = other

    @property
    def From(self):
        """发件人"""
        return self.__box.get("From")

    @From.setter
    def From(self, other):
        """发件人"""
        self.__check_str(other)
        self.__box["From"] = other

    @property
    def To(self):
        """收件人"""
        return self.__box.get("To")

    @To.setter
    def To(self, other):
        """收件人"""

        self.__check_str(other)
        self.__box["To"] = other

    @property
    def Cc(self):
        """抄送人"""
        return self.__box.get("Cc")

    @Cc.setter
    def Cc(self, other):
        """抄送人"""
        self.__check_str(other)
        self.__box["Cc"] = other

    @staticmethod
    def _packed(mime: MIMEBase, msg):
        mime.attach(msg)

    @staticmethod
    def __check_str(data):
        if not isinstance(data, str):
            raise MailTypeError(f"传入的参数类型有误, 应为`str`,实际为`{type(data)}`")

    @classmethod
    def __base_text(cls, msg, subtype):
        cls.__check_str(msg)
        item = MIMEBase("text", subtype)
        item.set_payload(msg, 'utf-8')
        return item

    def html(self, msg: str):
        """html内容, 与text同时存在时, 优先级较高

        Args:
            msg (str): html文本内容
        """
        item = self.__base_text(msg, 'html')
        self._packed(self.__cnt, item)

    def text(self, msg: str):
        """text内容,  与html同时存在时, 优先级较低

        Args:
            msg (str): text文本内容
        """
        item = self.__base_text(msg, 'plain')
        self._packed(self.__cnt, item)

    def file(self, filepath: str, name=None):
        """选择文件添加附件

        Args:
            filepath (str): 文件路径
            name (_type_, optional): 文件在邮件中显示的名字. 为None时显示原文件名.
        """
        if not isinstance(filepath, str):
            raise MailTypeError(f"传入的参数类型有误,  应为`str`,实际为`{type(filepath)}`")
        with open(filepath, 'rb') as f:
            self.byte(
                f.read(), name if name is not None else os.path.basename(filepath))

    def byte(self, data, name):
        """选择添加二进制数据

        Args:
            data (bytes): 二进制数据
            name (str): 数据在邮件中显示的名字

        """
        if not isinstance(data, bytes):
            raise MailTypeError(f"传入的参数类型有误,  应为`bytes`,实际为`{type(data)}`")
        item = MIMEBase("application", "octet-stream")
        item.set_payload(data)
        item.add_header('Content-Disposition', 'attachment', filename=name)
        encode_base64(item)
        self._packed(self.__box, item)

    def embed_img(self, data: bytes):
        """在html中插入图片

        Args:
            data (bytes): 二进制数据

        Returns:
            str: 随机生成的cid, 需要添加在html文本中以显示
        """
        if not isinstance(data, bytes):
            raise MailTypeError(f"传入的参数类型有误,  应为`bytes`,实际为`{type(data)}`")
        img_id = gener_random()
        item = MIMEBase("image", "*")
        item.set_payload(data)
        item.add_header("Content-ID", f"<{img_id}>")
        encode_base64(item)
        self._packed(self.__msg, item)
        return img_id

    def as_string(self):
        """最终发送邮件时, 转化为字符串

        Returns:
            str: 纯文本内容
        """
        return self.__box.as_string()


class Mail(MailContent):
    """通用邮件

    Args:
        from_addr (str): 发件地址
        to_addr (list[str]): 收件地址
    """

    _type = ''

    def __init__(
        self,
        from_addr: str,
        to_addr: list[str],
        bcc: bool = False,
        auto_retry: int = 0
    ) -> None:
        super().__init__()
        self.to_list = to_addr
        self.From = from_addr
        if not bcc:
            self.To = ','.join(to_addr)
        self.__retry = auto_retry
        self.__smtp = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_info, exc_trackback):
        self.quit()


    def connect(self, host: str, port: int, username: str, password: str, timeout: float = 5, ssl: bool = True):
        """连接到smtp服务器

        Args:
            host (str): smtp服务器地址
            port (int): smtp服务器端口
            username (str): 用户名, 一般为邮箱
            password (str): 授权码
            timeout (float, optional): 超时时长. 默认 5.
            ssl (bool, optional): 是否开启ssl连接. 默认 True.
        """
        if self._type not in username:
            raise MailUserError("传入的用户名与所用类对象不匹配, 若无您所使用的邮箱类型, 请使用通用邮箱类对象`Mail`")

        smtp_type = smtplib.SMTP_SSL if ssl else smtplib.SMTP
        self.__smtp = smtp_type(host=host, timeout=timeout)
        self.__smtp.connect(host, port)
        self.__smtp.ehlo(host)
        self.__smtp.login(username, password)

    def quit(self):
        """关闭与smtp服务器的会话
        """
        if self.__smtp is not None:
            self.__smtp.quit()

    def send(self):
        """
        发送邮件

        如果所有收件人均收件失败, 程序会报错. 除此之外的情况只会记录收件失败的信息
        """
        if self.__smtp is None:
            raise MailServerError("smtp服务未启动, 请先执行`connect(...)`")
        to = self.to_list if len(self.to_list) >= 2 else self.to_list.pop()

        result = self.__smtp.sendmail(self.From, to, self.as_string())
        return result

    def remail(self):
        f, t = self.From, self.to_list
        self.__dict__.clear()
        self.__init__(from_addr=f, to_addr=t)


class Mail163(Mail):
    _type = "163"
    def __init__(self, from_addr: str, to_addr: list[str]) -> None:
        super().__init__(from_addr, to_addr)

    def connect(self, username: str, password: str, timeout: float = 5, ssl: bool = True):
        return super().connect("smtp.163.com", 465, username, password, timeout, ssl)


class MailQQ(Mail):
    _type = "qq"
    def __init__(self, from_addr: str, to_addr: list[str]) -> None:
        super().__init__(from_addr, to_addr)

    def connect(self, username: str, password: str, timeout: float = 5, ssl: bool = True):
        return super().connect("smtp.qq.com", 465, username, password, timeout, ssl)
