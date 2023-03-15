"""Ingest and format quotes from text files"""

from typing import List
# from striprtf.striprtf import rtf_to_text

from .quote import Quote
from .ingestor import QuoteIngestor
from .exception import InvalidFileException, UnsupportedFileException

class TextQuotesIngestor(QuoteIngestor):
    """Quotes ingestor from text files"""

    @classmethod
    def whitelist(cls) -> List[str]:
        """Gets the allowed file extensions for ingesting quotes from text files"""

        return ["txt", "rtf"]

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Reads quotes from the path if it is a txt file"""

        parsed = []
        is_rtf = TextQuotesIngestor.extention(path) == 'rtf'
        if TextQuotesIngestor.handles(path):
            try:
                with open(path, encoding="UTF-8") as file:
                    for line in file:

                        text = line
                        if is_rtf:
                            # text = rtf_to_text(line)
                            text = line

                        parts = [txt.strip() for txt in text.split("-")]
                        quote = Quote(parts[0], parts[1])
                        parsed.append(quote)
            except (OSError, IOError) as err:
                raise InvalidFileException(path) from err
        else:
            raise UnsupportedFileException(path)

        return parsed
        