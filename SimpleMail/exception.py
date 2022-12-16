class MailError(Exception):
    message = "出现了一个未知错误"
    
    def __init__(self, message=None):
        if message:
            self.message = message

class ConfigError(MailError):
    message = "配置项出现错误或未配置 -> `{}`"
    
    def __init__(self, item):
        self.message = self.message.format(item)

class MailTypeError(MailError):
    def __init__(self, message):
        super().__init__(message)

class MailSendingError(MailError):
    def __init__(self, message):
        super().__init__(message)