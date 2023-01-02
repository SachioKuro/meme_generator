"""This file contains the TxtIngestor class which is used to ingest .txt files."""

from pathlib import Path

from quote_engine.ingestors.ingestor_interface import IngestorInterface
from quote_engine.models.quote_model import QuoteModel


class TXTIngestor(IngestorInterface):
    """Ingestor for .txt files."""

    allowed_extensions = ['.txt']

    @classmethod
    def parse(cls, path: Path) -> list[QuoteModel]:
        """Parse a TXT file and return a list of QuoteModel items."""
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception')

        quotes: list[QuoteModel] = []
        with open(path, 'r') as file:
            for line in file.readlines():
                if line.strip():
                    body, author = cls._split_on_last_dash(line)
                    body: str = body.strip('" ')
                    author: str = author.strip()

                    quotes.append(QuoteModel(body, author))

        return quotes
