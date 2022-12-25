class MailError(Exception):
    message = "出现了一个未知错误"
    
    def __init__(self, message=None):
        if message:
            self.message = message

class MailTypeError(MailError):
    def __init__(self, message):
        super().__init__(message)

class MailServerError(MailError):
    def __init__(self, message):
        super().__init__(message)

class MailUserError(MailError):
    def __init__(self, message):
        super().__init__(message)
