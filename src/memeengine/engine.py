"""The meme engine module, responsible for manipulating and drawing text onto images"""

from datetime import datetime
from os import path as ospath

from PIL import Image
from quoteengine import Quote
from .exceptions import MemeGenerationException


class Engine():
    """Engine for generating memes from images and texts"""

    _max_width = 500

    def __init__(self, base='./tmp') -> None:
        self.base_dir = base

    def resize(self, img: Image) -> Image:
        """Resizes the image to a max with of 500px, while keeping the aspect ratio"""

        wpercent = self._max_width / float(img.size[0])
        hsize = int((float(img.size[1]) * float(wpercent)))
        resized = img.resize((self._max_width, hsize),
                             Image.Resampling.LANCZOS)
        return resized

    def generate(self, img_path: str, quote: Quote) -> str:
        """
        Generates a meme using the provided image file and quote
        """

        generated = ""
        try:
            img = Image.open(img_path)
            img = self.resize(img)

            _, fext = ospath.splitext(img_path)
            meme_file = ospath.join(
                self.base_dir, f"{datetime.now().timestamp()}{fext}")
            img.save(meme_file)
            generated = meme_file
        except (OSError, IOError) as err:
            raise MemeGenerationException(img_path) from err

        return generated
