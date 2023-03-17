"""Turbo meme generator - core entrypoint"""

import os
import random

import filetype
from argparse import ArgumentParser

from memeengine import MemeEngine
from quoteengine import SmartIngestor, Quote

_IMAGES_DIR = "./_data/photos/dog/"
_QUOTES_DIR = "./_data/DogQuotes/"

def get_quote_for_meme(body, author, quotes_dir):
    quote = None

    if body is None:
        quotes = []
        quote_files = []
        for root, dirs, files in os.walk(quotes_dir):
            quote_files = [os.path.join(root, name) for name in files]

        for file in quote_files:
            quotes.extend(SmartIngestor.parse(file))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError('author is required when body is provided')
        quote = Quote(body, author)

    return quote

def get_img_for_meme(path, images_dir):
    img = None
    images = filetype.image_matchers
    if path is None:
        # images_dir will be "./_data/photos/dog/" or
        # a directory of custom images specified by the user
        imgs = []
        for root, dirs, files in os.walk(images_dir):
            # pull all the files
            imgs = [os.path.join(root, name) for name in files]
            # only the image files
            imgs = [file for file in imgs if filetype.match(file, matchers=images) is not None]

        img = random.choice(imgs)
    else:
        if filetype.match(path, matchers=images) is not None:
            img = path
        else:
            raise ValueError("path does not appear to be a valid image file")
    
    return img

def generate_meme(path=None, body=None, author=None, images=_IMAGES_DIR, quotes=_QUOTES_DIR):
    """ Generate a meme given an path and a quote """

    images_dir = _IMAGES_DIR if images is None else images
    img = get_img_for_meme(path, images_dir)

    quotes_dir = _QUOTES_DIR if quotes is None else quotes
    quote = get_quote_for_meme(body, author, quotes_dir)

    meme = MemeEngine('./generated/memes')
    generated_img = meme.generate(img, quote.body, quote.author)
    return generated_img


if __name__ == "__main__":

    cli = ArgumentParser()
    cli.add_argument('-p', '--path', help="Relative path to the image to generate the meme with")
    cli.add_argument('-b', '--body', help="The text body to use as quote message")
    cli.add_argument('-a', '--author', help="The author of the quote. Required if a quote is specified with -b | --body")
    cli.add_argument('--images', help="Relative directory path to your collection of images")
    cli.add_argument('--quotes', help="Relative directory path to your collection of quotes")

    args = cli.parse_args()
    generated = generate_meme(args.path, args.body, args.author, args.images, args.quotes)
    print(generated)
