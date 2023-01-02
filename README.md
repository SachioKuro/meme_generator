# MemeGenerator

MemeGenerator is a pyhton application which generates memes using the commandline or a flask app.

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements
```

## Usage

### Commandline

The arguments path, body and author are optional and a random one will be used if not supplied.

```bash
python3 meme.py --path --body --author
```

### WebApp

```bash
python3 app.py
```

## Briefing

The quote_engine module handles the parsing of several filetypes through ingestors to get quotes
from them.
Currently txt, csv, pdf and docx files are supported.
The meme_generator module takes an image and a quote to generate memes and save them to disc.
