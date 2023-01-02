"""This file contains the base class for all ingestors."""

from pathlib import Path
from quote_engine.ingestors.ingestor_interface import IngestorInterface
from quote_engine.ingestors.docx_ingestor import DocxIngestor
from quote_engine.ingestors.csv_ingestor import CSVIngestor
from quote_engine.ingestors.pdf_ingestor import PDFIngestor
from quote_engine.ingestors.txt_ingestor import TXTIngestor
from quote_engine.models.quote_model import QuoteModel


class Ingestor(IngestorInterface):
    """Ingestor class to ingest quotes from different file types."""

    ingestors: list[IngestorInterface] = [
        DocxIngestor(),
        CSVIngestor(),
        PDFIngestor(),
        TXTIngestor()
    ]

    @classmethod
    def parse(cls, path: Path) -> list[QuoteModel]:
        """Parse quotes from a file."""
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        print(f'Cannot ingest file: {path}')
        raise Exception('Cannot ingest file type.')
