"""Tempest exceptions module.
This module defines custom exceptions for the Tempest SDK.
The exceptions are used to handle errors and provide meaningful error messages
when interacting with the Tempest API.
"""


class TempestBaseException(Exception):
    """Base class for all Tempest exceptions.
    This class is the base exception for all exceptions raised by the Tempest SDK.
    It inherits from the built-in Exception class and provides a custom message
    and optional arguments.
    """


class TempestException(TempestBaseException):
    """Exception raised for Tempest API errors.
    This exception is raised when the Tempest API returns an error response.
    Attributes:
        http_status (int): The HTTP status code returned by the API.
        code (str): The error code returned by the API.
        msg (str): The error message returned by the API.
        reason (str, optional): The reason for the error.
        headers (dict, optional): Additional headers returned by the API.
    """

    def __init__(
        self,
        http_status: int,
        code: str,
        msg: str,
        reason: str | None = None,
        headers: dict | None = None,
    ):
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
        return (
            f"http status: {self.http_status}, "
            f"code: {self.code} - {self.msg}, "
            f"reason: {self.reason}"
        )


class TempestOauthException(TempestBaseException):
    """Exception raised for OAuth errors.
    This exception is raised when there is an error with the OAuth process.
    Attributes:
        message (str): The error message.
        error (str): The error code returned by the OAuth server.
        error_description (str): A description of the error.
        args (tuple): Additional arguments.
        kwargs (dict): Additional keyword arguments.
    """

    def __init__(
        self,
        message: str,
        error: str | None = None,
        error_description: str | None = None,
        *args: tuple,
        **kwargs: dict,
    ):
        self.error = error
        self.error_description = error_description
        self.__dict__.update(kwargs)
        super().__init__(message, *args, **kwargs)
