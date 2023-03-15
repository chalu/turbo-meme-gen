"""Turbo meme generator - core entrypoint"""

import os
import random

from memeengine import MemeEngine
from quoteengine import SmartIngestor, Quote

# @TODO Import your Ingestor and MemeEngine classes


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path[0]

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                    #    './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for file in quote_files:
            quotes.extend(SmartIngestor.parse(file))

        quote = random.choice(quotes)
    else:
        if author is None:
            raise ValueError('Author is required if Body is Used')
        quote = Quote(body, author)

    meme = MemeEngine('./generated/memes')
    generated_img = meme.generate(img, quote.body, quote.author)
    print(generated_img)
    return generated_img


if __name__ == "__main__":
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    # args = None
    # print(generate_meme(args.path, args.body, args.author))
    generate_meme()
