import os

import filetype

from quoteengine import SmartIngestor, Quote

class Utils():

    def get_quotes_for_meme(quotes_dir, body=None, author=None):
        quotes = []

        if body is None:
            quote_files = []
            for root, _, files in os.walk(quotes_dir):
                quote_files = [os.path.join(root, name) for name in files]

            for file in quote_files:
                quotes.extend(SmartIngestor.parse(file))

        else:
            if author is None:
                raise ValueError('author is required when body is provided')
            quotes = [Quote(body, author)]

        return quotes

    def get_imgs_for_meme(images_dir, path=None):
        imgs = []
        images = filetype.image_matchers
        if path is None:
            # images_dir will be "./_data/photos/dog/" or
            # a directory of custom images specified by the user
            for root, _, files in os.walk(images_dir):
                # pull all the files
                imgs = [os.path.join(root, name) for name in files]
                # only the image files
                imgs = [file for file in imgs if filetype.match(file, matchers=images) is not None]

        else:
            if filetype.match(path, matchers=images) is not None:
                imgs = [path]
            else:
                raise ValueError("path does not appear to be a valid image file")

        return imgs