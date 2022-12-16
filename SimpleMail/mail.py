import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from .utils import gener_random, create
from .exception import *

def send(subject: str, message: str, from_: str, password: str, to_: list, host: str, port: int):
    mail = Mail(from_, from_, password)
    mail.connect(host, port)
    msg = TEXTMail(message, to_)
    msg.subject(subject)
    # msg.header(subject, )
    mail.send(msg)


class MailMEssage:
    def __init__(self, message: str, receiver: str | list, maintype, subtype, subject: str | None = None) -> None:
        if isinstance(receiver, str):
            if "@" not in receiver:
                raise MailTypeError(f"邮件格式错误 (error:({receiver}))")
            self.receiver = [receiver]
        elif isinstance(receiver, list):
            if not all("@" in rece for rece in receiver):
                e = [i for i in receiver if "@" not in i]
                raise MailTypeError(f"邮件格式错误 (error:({e}))")
            self.receiver = receiver
        else:
            raise TypeError("`receiver` is not a `str` or `list`")
        
        self._main = MIMEMultipart("alternative")
        sub = MIMEBase(maintype, subtype)
        sub.set_payload(message, 'utf-8')
        self._main.attach(sub)
        if subject is not None:
            self._main["Subject"] = subject

    def __repr__(self) -> str:
        return f'{self._main.get("Subject"):^{40}}\n\n{self._main}\n{"Sender:"+str(self.receiver):>{40}}'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_info, exc_tb):
        pass


    def subject(self, subject: str, set_from: str | None = None, set_to: list | None = None):

        self._main["Subject"] = subject
        if set_from is not None:
            self._main["From"] = set_from
        if set_to is not None:
            self._main["To"] = ",".join(set_to)

    def file(self, file_path: str, file_name: str | None = None):
        sub = create(file_path, file_name, True)
        self._main.attach(sub)

    def data(self, data: bytes, name):
        sub = create(data, name, True)
        self._main.attach(sub)


class TEXTMail(MailMEssage):
    def __init__(self, message: str, receiver: str | list[str], subject: str | None = None) -> None:
        super().__init__(message, receiver, "text", "html", subject)


class HTMLMail(MailMEssage):
    def __init__(self, message: str, receiver: str | list[str], subject: str | None = None) -> None:
        super().__init__(message, receiver, "text", "plain", subject)

    @staticmethod
    def add_image(data: bytes) -> str:
        if isinstance(data, bytes):
            sub = create(data, "")
            img_id = gener_random()
            sub.add_header('Content-ID', f'<{img_id}>')
            return f'<img src="cid:{img_id}" alt="image:{img_id}">'
        else:
            raise TypeError("`data` is not a `bytes`")


class Mail:
    mailtype = ""

    def __init__(
        self,
        sender: str,
        username: str,
        password: str
    ) -> None:
        self.user = username
        self.sender = sender
        self.pwd = password
        if not self.check_mail_type():
            raise MailTypeError("请检查邮箱账号所属服务商(@xxxx.com)是否与使用类(Mailxxxx)匹配")

    @classmethod
    def html(cls, message: str, receiver: str | list[str], subject: str | None = None):
        return HTMLMail(message, receiver, subject)

    @classmethod
    def text(cls, message: str, receiver: str | list[str], subject: str | None = None):
        return TEXTMail(message, receiver, subject)

    def check_mail_type(self) -> bool:
        if self.mailtype in self.sender:
            return True
        return False

    def connect(
        self,
        host: str,
        port: int,
        is_ssl: bool = True,
        timeout: float = 5,
    ) -> list:
        msg = []
        smtp_type = smtplib.SMTP_SSL if is_ssl else smtplib.SMTP
        smtp = smtp_type(host=host, timeout=timeout)
        msg.append(smtp.connect(host=host, port=port))
        msg.append(smtp.ehlo(host))
        msg.append(smtp.login(self.user, self.pwd))
        self.smtp = smtp
        return msg

    def send(self, message: MailMEssage) -> dict:
        if not hasattr(self, "smtp"):
            raise MailSendingError("SMTP连接错误，请先执行`connect(...)`")
        
        result = self.smtp.sendmail(
            self.sender,
            message.receiver,
            message._main.as_string()
        )
        self.smtp.quit()
        return result


class MailQQ(Mail):
    mailtype = "qq.com"

    def __init__(self, sender: str, username: str, password: str) -> None:
        super().__init__(sender, username, password)

    def connect(self, is_ssl: bool = True, timeout: float = 5) -> list:
        return super().connect("smtp.qq.com", 465, is_ssl, timeout)


class Mail163(Mail):
    mailtype = "163.com"

    def __init__(self, sender: str, username: str, password: str) -> None:
        super().__init__(sender, username, password)

    def connect(self, _is_ssl: bool = True, _timeout: float = 5) -> list:
        return super().connect("smtp.163.com", 465, _is_ssl, _timeout)
