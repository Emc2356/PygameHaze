class BaseException(Exception):
    """
    the base exception for the rest of the exception
    that are used for this package
    """
    pass


class TextOutOfButton(BaseException):
    """
    the exception that is raised when the
    text that is used in the button is out of
    the bounds of the button
    """
    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return repr(self.message)


__all__ = [
    "TextOutOfButton"
]
