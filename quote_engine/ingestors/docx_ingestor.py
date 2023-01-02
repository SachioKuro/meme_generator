"""This file contains the DocxIngestor class which is responsible for ingesting docx files."""

import docx
from pathlib import Path

from quote_engine.ingestors.ingestor_interface import IngestorInterface
from quote_engine.models.quote_model import QuoteModel


class DocxIngestor(IngestorInterface):
    """Ingestor for doc files."""

    allowed_extensions = ['.docx']

    @classmethod
    def parse(cls, path: Path) -> list[QuoteModel]:
        """Parse a DOCX file and return a list of QuoteModel items."""
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest exception')

        quotes: list[QuoteModel] = []
        doc = docx.Document(path)
        for paragraph in doc.paragraphs:
            if paragraph.text:
                body, author = cls._split_on_last_dash(paragraph.text)
                body: str = body.strip('" ')
                author: str = author.strip()

                quotes.append(QuoteModel(body, author))

        return quotes
