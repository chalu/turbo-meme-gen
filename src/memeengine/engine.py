"""The meme engine module, responsible for manipulating and drawing text onto images"""

from datetime import datetime
from os import path as ospath, makedirs

from PIL import Image, ImageDraw, ImageFont
from .exceptions import MemeGenerationException


class Engine():
    """Engine for generating memes from images and texts"""

    _max_width = 500
    _font_path = './_data/fonts/RobotoMono-Regular.ttf'

    def __init__(self, base='./tmp') -> None:
        self.base_dir = base
        self.txt_font = ImageFont.truetype(self._font_path, 20)

    def _resize(self, img: Image, width: int) -> Image:
        """Resizes the image to a max with of 500px, while keeping the aspect ratio"""

        wpercent = width / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        resized = img.resize((width, hsize), Image.Resampling.LANCZOS)
        return resized

    def _draw(self, img: Image, text) -> Image:
        """Draw the quote over the image"""
        img_w, img_h = img.size

        draw = ImageDraw.Draw(img)
        text_w, text_h = draw.textsize(text, font=self.txt_font)

        margin = 50
        pos_x = img_w - text_w - margin
        pos_y = img_h - text_h - margin
        position = (pos_x, pos_y)

        box_pad = 15
        expand = box_pad * 2
        negated = (position[0] - box_pad, position[1] - box_pad)
        bbox = draw.textbbox(negated, text, font=self.txt_font)
        expanded = (bbox[0], bbox[1], bbox[2] + expand, bbox[3] + expand)
        draw.rectangle(expanded, fill=(0, 0, 0))

        draw.text(position, text, (255, 255, 255), font=self.txt_font)

        return img

    def generate(self, img_path: str, quote: str, author: str, width=500) -> str:
        """
        Generates a meme using the provided image file and quote
        """

        generated = ""
        try:
            img = Image.open(img_path)
            text = f"{quote}\n- {author}"

            img = self._resize(img, min(width, self._max_width))
            img = self._draw(img, text)

            _, fext = ospath.splitext(img_path)
            fname = f"{datetime.now().timestamp()}{fext}"
            if ospath.exists(self.base_dir) is False:
                makedirs(self.base_dir)
            meme_file = ospath.join(self.base_dir, fname)

            img.save(meme_file)
            generated = meme_file
        except (OSError, IOError) as err:
            raise MemeGenerationException(img_path) from err

        return generated
