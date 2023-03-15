"""The meme engine module, responsible for manipulating and drawing text onto images"""

from PIL import Image

from quoteengine import Quote

class Engine():
    """Engine for generating memes from images and texts"""

    def __init__(self, base='./tmp') -> None:
        self.base_dir = base

    def generate(self, img_path:str, quote: Quote) -> str:
        """
        Generates a meme using the provided image file and quote
        """
        return img_path
