"""An abstract ingestor class for quotes."""

from typing import List
from abc import ABC, abstractmethod

from .quote import Quote


class QuoteIngestor(ABC):
    """Abstract ingestor that concrete ingestors must implement."""

    @classmethod
    def invalids(cls) -> str:
        """Get invalid leading/lagging char to strip from quotes."""
        return " \"\'"

    @classmethod
    def extention(cls, path: str) -> str:
        """Return the extension of the file indicated with path."""
        return path.split('.')[-1]

    @classmethod
    def handles(cls, path: str) -> bool:
        """Return true if path has supported extension, else false."""
        ext = cls.extention(path)
        return ext in cls.whitelist()

    @classmethod
    @abstractmethod
    def whitelist(cls) -> List[str]:
        """Get allowed file extensions."""
        return [""]

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[Quote]:
        """Read quotes from path if supported."""
        return [""]
