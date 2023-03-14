"""Ingest and format quotes from CSV files"""

from typing import List
from os import path as ospath
from csv import DictReader as reader

from .quote import Quote
from .ingestor import QuoteIngestor


class CSVQuotesIngestor(QuoteIngestor):
    """Quotes ingestor from CSV files"""

    @classmethod
    def whitelist(cls) -> List[str]:
        """Gets the allowed file extensions for ingesting quotes from CSV files"""

        return ["csv"]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Reads quotes from the path if it is a CSV file"""

        parsed = []
        if CSVQuotesIngestor.handles(path):
            try:
                with open(path, encoding="UTF-8") as file:
                    data = reader(file, delimiter=',',
                                  fieldnames=['body', 'author'])
                    # move intot the rows with values, skipping the header
                    next(data)
                    for row in data:
                        quote = Quote(row['body'].strip(),
                                      row['author'].strip())
                        parsed.append(quote)
            except (OSError, IOError):
                head, tail = ospath.split(path)
                print(f"Failed to locate, open or read from: {tail} in {head}")

        return parsed
