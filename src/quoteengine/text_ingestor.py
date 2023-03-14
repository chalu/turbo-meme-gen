"""Ingest and format quotes from text files"""

from typing import List
from os import path as ospath
# from striprtf.striprtf import rtf_to_text

from quoteengine import Quote
from .ingestor import QuoteIngestor

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
            except (OSError, IOError):
                head, tail = ospath.split(path)
                print(f"Failed to locate, open or read from: {tail} in {head}")
            # except Exception:
            #     head, tail = ospath.split(path)
            #     print(f"Failed to parse quotes from: {tail} in {head}")

        return parsed
        