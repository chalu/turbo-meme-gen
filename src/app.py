import os
import random
import requests
from datetime import datetime

from utilities import Utils
from memeengine import MemeEngine
from flask import Flask, render_template, abort, request as req

_IMAGES_DIR = "./_data/photos/dog/"
_QUOTES_DIR = "./_data/DogQuotes/"

app = Flask(__name__)
meme = MemeEngine('./static')

def setup():
    """ Load all resources """

    quotes = Utils.get_quotes_for_meme(_QUOTES_DIR)
    imgs = Utils.get_imgs_for_meme(_IMAGES_DIR)

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.generate(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ Take user input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    img = "https://placehold.co/500x500?text=Something+Went+Wrong"

    image_url = req.form['image_url'].strip()
    body  = req.form['body'].strip()
    author = req.form['author'].strip()

    img_file = None
    r = requests.get(image_url, stream=True, allow_redirects=True)
    if r.status_code == 200:
        _, fext = os.path.splitext(image_url)
        img_file = f"{datetime.now().timestamp()}{fext}"
        with open(img_file, 'wb') as f:
            f.write(r.content)

    if img_file is not None:
        img = meme.generate(img_file, body, author)
        os.remove(img_file)

    return render_template('meme.html', path=img)

if __name__ == "__main__":
    app.run()
