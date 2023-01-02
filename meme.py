"""This file is responsible for the meme command line interface."""

import argparse
import os
from pathlib import Path
import random

from quote_engine.ingestors.ingestor import Ingestor
from quote_engine.models.quote_model import QuoteModel
from meme_engine.meme_generator import MemeGenerator


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path, a quote body and author."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, _, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = [Path('./_data/DogQuotes/DogQuotesTXT.txt'),
                       Path('./_data/DogQuotes/DogQuotesDOCX.docx'),
                       Path('./_data/DogQuotes/DogQuotesPDF.pdf'),
                       Path('./_data/DogQuotes/DogQuotesCSV.csv')]
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = QuoteModel(body, author)

    meme = MemeGenerator(Path('./tmp'))
    path = meme.make_meme(Path(img), quote.body, quote.author)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a meme')
    parser.add_argument('--path', type=str, help='path to an image file')
    parser.add_argument('--body', type=str, help='quote body to add to the image')
    parser.add_argument('--author', type=str, help='quote author to add to the image')
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
