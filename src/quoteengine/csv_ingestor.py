"""Ingest and format quotes from CSV files"""

from typing import List
from csv import DictReader as reader

from .quote import Quote
from .ingestor import QuoteIngestor
from .exceptions import InvalidFileException, UnsupportedFileException


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
                    # move into the rows with values, skip the header row
                    next(data)

                    invalid_chars = CSVQuotesIngestor.invalids()
                    for row in data:
                        quote = Quote(row['body'].strip(invalid_chars),
                                      row['author'].strip(invalid_chars))
                        parsed.append(quote)
            except (OSError, IOError) as err:
                raise InvalidFileException(path) from err
        else:
            raise UnsupportedFileException(path)

        return parsed
