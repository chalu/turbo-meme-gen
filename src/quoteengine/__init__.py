"""
The quote engine module
Handles ingesting, parsing and properly formatting quotes from
a variety of file formates into a unified Quote model object
"""

from .quote import Quote
from .csv_ingestor import CSVQuotesIngestor
from .text_ingestor import TextQuotesIngestor
from .docx_ingestor import DocxQuotesIngestor
from .smart_ingestor import SmartIngestor
