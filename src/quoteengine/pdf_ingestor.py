"""Ingest and format quotes from PDF files"""

import subprocess as sp
from typing import List
from datetime import datetime
from os import remove as delete_file

from .quote import Quote
from .ingestor import QuoteIngestor
from .exceptions import InvalidFileException, UnsupportedFileException


class PDFQuotesIngestor(QuoteIngestor):
    """
    Quotes ingestor from PDF files
    Uses subprocess to call the pdftotext program from the xpdf CLI tools.
    See https://www.xpdfreader.com/about.html
    """

    @classmethod
    def whitelist(cls) -> List[str]:
        """Gets the allowed file extensions for ingesting quotes from PDF files"""

        return ["pdf"]

    def pdftotext(self, path, out_file):
        #Generate a text rendering of a PDF file in the form of a list of lines.
        args = ['pdftotext', '-layout', path, out_file]
        cp = sp.run(
            args, stdout=sp.PIPE, stderr=sp.DEVNULL,
            check=True, text=True
        )
        return cp.stdout

    @classmethod
    def parse(cls, path: str) -> List[Quote]:
        """Reads quotes from the path if it is a PDF file"""

        parsed = []
        if PDFQuotesIngestor.handles(path):
            try:
                # Generate a text rendering of the PDF file as a list of lines.
                temp_txt_file = f"./_data/{datetime.now().timestamp()}.txt"
                args = ['pdftotext', '-layout', path, temp_txt_file]
                sp.run(
                    args, stdout=sp.PIPE, stderr=sp.DEVNULL,
                    check=True, text=True
                )

                with open(temp_txt_file, encoding="UTF-8") as file:
                    for line in file:
                        parts = [pt.strip(PDFQuotesIngestor.invalids) for pt in line.split("-")]
                        if len(parts) < 2:
                            continue

                        parsed.append(Quote(parts[0], parts[1]))
                delete_file(temp_txt_file)
            except (OSError, IOError) as err:
                raise InvalidFileException(path) from err
        else:
            raise UnsupportedFileException(path)

        return parsed
