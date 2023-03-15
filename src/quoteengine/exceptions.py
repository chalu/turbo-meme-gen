"""Exceptions that can be raised while handling quote files"""

from os import path as ospath

class QuotesFileException(ValueError):
    """Base exception raised while handling a quotes file.

    Attributes:
        path -- path to the file been processed for quotes
        message -- optional error message for client code
    """

    def __init__(self, path: str, message: str = "") -> None:
        self.path = path
        head, tail = ospath.split(path)
        self.loc = head
        self.filename = tail

        self.message = message
        if self.message == "":
            self.message = f"Failed to handle file: {self.filename} in {self.loc}"

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

class InvalidFileException(QuotesFileException):
    """Exception raised from errors while parsing a quotes file.

    Attributes:
        path -- path to the file been processed for quotes
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.message = f"Failed to locate, open or read from: {self.filename} in {self.loc}"

    def __str__(self) -> str:
        return self.message

class UnsupportedFileException(QuotesFileException):
    """Exception raised if the file is not a supported file format.

    Attributes:
        path -- path to the file been processed for quotes
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.message = f"Failed to locate, open or read from: {self.filename} in {self.loc}"

    def __str__(self) -> str:
        return self.message
