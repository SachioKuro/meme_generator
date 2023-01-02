"""This file contains the CSVIngestor class which is used to ingest CSV files."""

import csv
from pathlib import Path

from quote_engine.ingestors.ingestor_interface import IngestorInterface
from quote_engine.models.quote_model import QuoteModel


class CSVIngestor(IngestorInterface):
    """Ingestor for CSV files."""

    allowed_extensions = ['.csv']

    @classmethod
    def parse(cls, path: Path) -> list[QuoteModel]:
        """Parse a CSV file."""
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception.')

        quotes = []

        with open(path, 'r') as file:
            reader = csv.reader(file)
            for body, author in reader:
                body = body.strip('" ')
                author = author.strip()

                quotes.append(QuoteModel(body, author))

        return quotes
