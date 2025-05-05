class TempestBaseException(Exception):
    pass


class TempestException(TempestBaseException):

    def __init__(self, http_status, code, msg, reason=None, headers=None):
        self.http_status = http_status
        self.code = code
        self.msg = msg
        self.reason = reason
        # `headers` is used to support `Retry-After` in the event of a
        # 429 status code.
        if headers is None:
            headers = {}
        self.headers = headers

    def __str__(self):
        return (f"http status: {self.http_status}, "
                f"code: {self.code} - {self.msg}, "
                f"reason: {self.reason}")


class TempestOauthException(TempestBaseException):
    
    def __init__(self, message, error=None, error_description=None, *args, **kwargs):
        self.error = error
        self.error_description = error_description
        self.__dict__.update(kwargs)
        super().__init__(message, *args, **kwargs)
