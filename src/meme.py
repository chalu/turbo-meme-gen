"""Turbo meme generator - core entrypoint."""
import random
from argparse import ArgumentParser

from utilities import Utils
from memeengine import MemeEngine

_IMAGES_DIR = "./_data/photos/dog/"
_QUOTES_DIR = "./_data/DogQuotes/"


def generate_meme(path=None, body=None, author=None, images=None, quotes=None):
    """Generate a meme given an path and a quote."""
    images_dir = _IMAGES_DIR if images is None else images
    imgs = Utils.get_imgs_for_meme(images_dir, path)
    img = random.choice(imgs)

    quotes_dir = _QUOTES_DIR if quotes is None else quotes
    qts = Utils.get_quotes_for_meme(quotes_dir, body, author)
    quote = random.choice(qts)

    meme = MemeEngine('./static')
    generated_img = meme.generate(img, quote.body, quote.author)
    return generated_img


if __name__ == "__main__":

    cli = ArgumentParser()
    cli.add_argument('-p', '--path', help="Relative path to the source image")
    cli.add_argument('-b', '--body', help="Text body for quote message")
    cli.add_argument(
        '-a', '--author',
        help="Author of the quote. Required if -b | --body is used"
    )
    cli.add_argument('--images', help="Your custom images dir")
    cli.add_argument('--quotes', help="Your custom quotes dir")

    args = cli.parse_args()
    generated = generate_meme(
        args.path, args.body, args.author, args.images, args.quotes
    )
    print(generated)
