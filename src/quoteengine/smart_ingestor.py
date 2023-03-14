"""Ingest and format quotes from supported files"""

from typing import List
from os import path as ospath

from .quote import Quote
from .ingestor import QuoteIngestor
from .csv_ingestor import CSVQuotesIngestor as CsvIngest
from .docx_ingestor import DocxQuotesIngestor as DocxIngest
from .text_ingestor import TextQuotesIngestor as TextIngest


class SmartIngestor(QuoteIngestor):
    """Quotes ingestor from any/all supported file"""

    @classmethod
    def ingestors(cls) -> List[QuoteIngestor]:
        return [TextIngest, CsvIngest, DocxIngest]

    @classmethod
    def whitelist(cls) -> List[str]:
        """Gets the allowed file extensions for ingesting quotes from text files"""

        return [
            ext
            for ing in SmartIngestor.ingestors()
            for ext in ing.whitelist()
        ]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Reads quotes from the path if it is a supported file"""

        quotes = []
        if SmartIngestor.handles(path):
            try:
                # map extensions to their ingestors
                # e.g csv:CsvIngest, txt:TextIngest, and rtf:TextIngest
                mapping = {
                    ext:ing
                    for ing in SmartIngestor.ingestors()
                    for ext in ing.whitelist()
                }

                ext = SmartIngestor.extention(path)
                ingestor = mapping[ext]
                if ingestor is not None:
                    quotes = ingestor.parse(path)
            except (OSError, IOError):
                head, tail = ospath.split(path)
                print(f"Failed to locate, open or read from: {tail} in {head}")

        return quotes
