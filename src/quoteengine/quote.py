"""The Quote model class"""

class Quote():
    """A model that encapsulates and represents a quote"""

    def __init__(self, bdy: str, author="") -> None:
        self._body = bdy
        self._author = author

    @property
    def body(self) -> str:
        """Access the text of the quote"""
        return self._body

    @body.setter
    def body(self, bdy: str) -> None:
        """Set the text of the quote"""
        self._body = bdy.strip()

    @property
    def author(self) -> str:
        """Access the author of the quote"""
        return self._author

    @author.setter
    def author(self, author: str) -> None:
        """Set the author of the quote"""
        self._author = author.strip()

    def __str__(self) -> str:
        return f'{self._body} - {self._author}'

    def __repr__(self) -> str:
        return self.__str__()
