"""This file contains the MemeGenerator class which is used to generate memes."""

import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


class MemeGenerator:
    """Class for generating memes."""

    def __init__(self, output_dir: Path) -> None:
        """Initialize the MemeGenerator class."""
        self.output_dir = output_dir

    def make_meme(self, img_path: Path, text: str, author: str, width=500) -> Path:
        """Create a meme given an image and text.

        :param img_path: The path to an image file
        :param text: The text to put on the image
        :param author: The author of the quote
        :param width: The width of the output image

        :return: The path to the output image.
        """
        width = 500 if width > 500 else width
        with Image.open(img_path) as img:
            img = img.resize((width, int(width * img.height / img.width)))
            font = ImageFont.truetype("./fonts/FiraCode-Bold.ttf", size=30)
            draw = ImageDraw.Draw(img)
            draw.text((0, 0), text, font=font, fill="red")
            draw.text((20, 30), f"- {author}", font=font, fill="black")
            output_path = self.output_dir / img_path.name
            try:
                if not self.output_dir.exists():
                    self.output_dir.mkdir(parents=True)
                img.save(output_path)
            except FileNotFoundError:
                logging.error(f'File not created correctly: {output_path}')
        return output_path
