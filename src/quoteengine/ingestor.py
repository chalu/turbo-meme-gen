"""An abstract ingestor class for quotes"""

from typing import List
from abc import ABC, abstractmethod

from .quote import Quote


class QuoteIngestor(ABC):
    """An abstract ingestor interface that concrete ingestors must implement"""

    # TODO why does @property have to come after @classmethod for ClassName.invalids to work
    @classmethod
    @property
    def invalids(cls) -> str:
        """Invalid leading/lagging characters that the ingestor can strip out of quotes"""
        return " \"\'"

    @classmethod
    def extention(cls, path: str) -> str:
        """Returns the extension of the file indicated with path"""
        return path.split('.')[-1]

    @classmethod
    def handles(cls, path: str) -> bool:
        """Returns true if this ingestor can parse files indicated in path, else false"""
        ext = cls.extention(path)
        return ext in cls.whitelist()

    @classmethod
    @abstractmethod
    def whitelist(cls) -> List[str]:
        """Gets the allowed file extensions for an ingestor. Pls override on a per-ingestor basis"""

        return [""]

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[Quote]:
        """Reads quotes from the path if supported. Pls override on a per-ingestor basis"""
        return [""]
