"""Ingest and format quotes from DOCX files."""

from typing import List
from docx import Document as DocX

from .quote import Quote
from .ingestor import QuoteIngestor
from .exceptions import InvalidFileException, UnsupportedFileException


class DocxQuotesIngestor(QuoteIngestor):
    """Quotes ingestor from DOCX files."""

    @classmethod
    def whitelist(cls) -> List[str]:
        """Get allowed DOCX file extensions."""
        return ["docx"]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Read quotes from path if it is a DOCX file."""
        parsed = []
        if DocxQuotesIngestor.handles(path):
            try:
                doc = DocX(path)
                invalid_chars = DocxQuotesIngestor.invalids()
                for line in doc.paragraphs:
                    parts = [part.strip(invalid_chars)
                             for part in line.text.split("-")]
                    if parts and len(parts) == 2:
                        quote = Quote(parts[0], parts[1])
                        parsed.append(quote)
            except (OSError, IOError) as err:
                raise InvalidFileException(path) from err
        else:
            raise UnsupportedFileException(path)

        return parsed
