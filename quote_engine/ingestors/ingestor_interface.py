"""This file contains the interface for ingestors."""

from abc import ABC, abstractmethod
from pathlib import Path

from quote_engine.models.quote_model import QuoteModel


class IngestorInterface(ABC):
    """Interface for ingestors to implement."""

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: Path) -> bool:
        """Check if the file extension is allowed."""
        return path.suffix in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: Path) -> list[QuoteModel]:
        """Parse and return a list of QuoteModel items."""
        pass

    @classmethod
    def _split_on_last_dash(cls, line: str) -> tuple[str, str]:
        """Split the line on the last dash."""
        return tuple(line.rsplit(" - ", 1))
