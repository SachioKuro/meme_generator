"""Module for QuoteModel class."""

from dataclasses import dataclass


@dataclass
class QuoteModel:
    """Class for holding quote data."""

    body: str
    author: str

    def __repr__(self):
        """Return machine readable representation of this quote."""
        return f'Quote<{self.body},{self.author}>'
