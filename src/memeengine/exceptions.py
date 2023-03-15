"""Exceptions that can be raised while generating memes with the meme engine"""

from os import path as ospath

class MemeEngineException(RuntimeError):
    """Base exception raised by errors from meme generation.

    Attributes:
        path -- path to the image file the meme is based on
        message -- optional error message for client code
    """

    def __init__(self, path: str, message: str = "") -> None:
        self.path = path
        head, tail = ospath.split(path)
        self.loc = head
        self.filename = tail

        self.message = message
        if self.message == "":
            self.message = f"Failed to make meme with file: {self.filename} in {self.loc}"

        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message

class MemeGenerationException(MemeEngineException):
    """Exception raised when generating a meme fails.

    Attributes:
        path -- path to the image file the meme is based on
    """

    def __init__(self, path: str) -> None:
        super().__init__(path)
        self.message = f"Failed to generate meme with file: {self.filename} in {self.loc}"

    def __str__(self) -> str:
        return self.message
