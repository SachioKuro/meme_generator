"""This file contains the main application code for the Flask app."""

from pathlib import Path
import random
import requests
import os
import shutil
import uuid
from flask import Flask, render_template, abort, request, Response

from meme_engine.meme_generator import MemeGenerator
from quote_engine.ingestors.ingestor import Ingestor
from quote_engine.models.quote_model import QuoteModel

app: Flask = Flask(__name__)

meme: MemeGenerator = MemeGenerator(Path("./static"))


def setup() -> tuple[list[QuoteModel], list[Path]]:
    """Load all resources."""
    quote_files: list[Path] = [
        Path("./_data/DogQuotes/DogQuotesTXT.txt"),
        Path("./_data/DogQuotes/DogQuotesDOCX.docx"),
        Path("./_data/DogQuotes/DogQuotesPDF.pdf"),
        Path("./_data/DogQuotes/DogQuotesCSV.csv"),
    ]

    quotes: list[QuoteModel] = [
        quote for file in quote_files for quote in Ingestor.parse(file)
    ]

    images_path: Path = Path("./_data/photos/dog/")

    # imgs = images_path.glob('*.jpg')
    imgs: list[Path] = [
        images_path / file for file in os.listdir(images_path) if file.endswith(".jpg")
    ]

    return quotes, imgs


quotes, imgs = setup()


@app.route("/")
def meme_rand() -> Response:
    """Generate a random meme."""
    img: Path = random.choice(imgs)
    quote: QuoteModel = random.choice(quotes)
    path: Path = meme.make_meme(img, quote.body, quote.author)
    return render_template("meme.html", path=path)


@app.route("/create", methods=["GET"])
def meme_form() -> Response:
    """User input for meme information."""
    return render_template("meme_form.html")


@app.route("/create", methods=["POST"])
def meme_post() -> Response:
    """Create a user defined meme."""
    image_url: str = request.form.get("image_url")
    body: str = request.form.get("body")
    author: str = request.form.get("author")

    uuid_hex = uuid.uuid4().hex

    if not Path("tmp/").is_dir():
        Path("tmp/").mkdir()

    req = requests.get(image_url, stream=True)
    if req.status_code == 200:
        with open(Path(f"tmp/{uuid_hex}.jpg"), "wb") as f:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, f)
    else:
        abort(req.status_code)

    path: Path = meme.make_meme(Path(f"tmp/{uuid_hex}.jpg"), body, author)

    if Path(f"tmp/{uuid_hex}.jpg").exists():
        Path(f"tmp/{uuid_hex}.jpg").unlink()

    return render_template("meme.html", path=path)


if __name__ == "__main__":
    app.run()
