"""
The Meme Engine module.

Responsible for manipulating and drawing text onto images
"""

from datetime import datetime
from os import path as ospath, makedirs

from textwrap3 import wrap
from PIL import Image, ImageDraw, ImageFont
from .exceptions import MemeGenerationException


class Engine():
    """Engine for generating memes from images and texts."""

    _max_width = 500
    _font_path = './_data/fonts/RobotoMono-Regular.ttf'

    def __init__(self, out_dir='./tmp') -> None:
        """Initialize the engine."""
        self.out_dir = out_dir
        self.txt_font = ImageFont.truetype(self._font_path, 20)

    def resize(self, img: Image, width: int) -> Image:
        """Resize the image to 500px max. Kepps the aspect ratio."""
        capped_width = min(width, self._max_width)
        wpercent = capped_width / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        return img.resize((capped_width, hsize), Image.Resampling.LANCZOS)

    def draw(self, img: Image, text) -> Image:
        """Draw the quote over the image."""
        img_w, img_h = img.size
        draw = ImageDraw.Draw(img)

        total_h = 0
        longest_w = 0
        longest_text = None
        wrapped = wrap(text, 30)
        for line in wrapped:
            text_w, text_h = draw.textsize(line, font=self.txt_font)
            total_h += text_h
            if text_w > longest_w:
                longest_w = text_w
                longest_text = line

        # space between textbox and image edges
        margin = 45

        # space between text and textbox edges
        padding = 18

        pos_x = img_w - longest_w - margin
        pos_y = img_h - total_h - margin
        position = (pos_x, pos_y)

        # adjustments needed for the text to be
        # properly positioned within the box
        expand = padding * 2
        negated = (position[0] - padding, position[1] - padding)

        bbox = draw.textbbox(negated, longest_text, font=self.txt_font)
        left, top, right, bottom = bbox
        expanded = (left, top, right + expand, bottom + total_h + padding)
        draw.rectangle(expanded, fill=(0, 0, 0))

        for line in wrapped:
            draw.text(position, line, (255, 255, 255), font=self.txt_font)
            pos_y += self.txt_font.getsize(line)[1]
            position = (pos_x, pos_y)

        return img

    def generate(
            self, img_path: str, quote: str, author: str, width=500
    ) -> str:
        """Generate a meme using the provided image file and quote."""
        generated = ""
        try:
            img = Image.open(img_path)
            text = f"{quote}\n- {author}"

            img = self.resize(img, width)
            img = self.draw(img, text)

            _, fext = ospath.splitext(img_path)
            fname = f"{datetime.now().timestamp()}{fext}"
            if ospath.exists(self.out_dir) is False:
                makedirs(self.out_dir)
            meme_file = ospath.join(self.out_dir, fname)

            img.save(meme_file)
            generated = meme_file
        except (OSError, IOError) as err:
            raise MemeGenerationException(img_path) from err

        return generated
