"""
简易邮件
~~~~~~~

使用
>>> import simplemail  /  from simplemail import Mail
>>> mail = Mail(sender, receiver)  // 创建mail对象
>>> mail.html(...)  // 添加html内容
>>> mail.file(...)  // 添加附件
>>> mail.connect(...)  // 连接smtp服务器
>>> mail.send()  // 发送邮件

或者

>>> with Mail(...) as mail:
>>>     ......
>>>     mail.send()
"""


from .mail import Mail, Mail163, MailQQ
from .utils import address
