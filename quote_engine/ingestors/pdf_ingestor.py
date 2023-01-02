"""This file contains the PDFIngestor class which is responsible for ingesting PDF files."""

from pathlib import Path
import subprocess

from quote_engine.ingestors.ingestor_interface import IngestorInterface
from quote_engine.models.quote_model import QuoteModel


class PDFIngestor(IngestorInterface):
    """Ingestor for PDF files."""

    allowed_extensions = ['.pdf']

    @classmethod
    def parse(cls, path: Path) -> list[QuoteModel]:
        """Parse a PDF file and return a list of QuoteModel items."""
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception')

        quotes: list[QuoteModel] = []
        with subprocess.Popen(['pdftotext', path, '-'], stdout=subprocess.PIPE) as proc:
            if proc.stdout is None:
                raise Exception('Cannot ingest exception')
            pdf = [line.decode('utf-8') for line in proc.stdout.readlines()]

        for line in pdf:
            if line.strip():
                body, author = cls._split_on_last_dash(line)
                body: str = body.strip('" ')
                author: str = author.strip()

                quotes.append(QuoteModel(body, author))

        return quotes
