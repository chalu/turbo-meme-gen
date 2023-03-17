# turbo-meme-gen

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/da280ea75920476280adc1c706ff5700)](https://www.codacy.com/gh/chalu/turbo-meme-gen/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=chalu/turbo-meme-gen&amp;utm_campaign=Badge_Grade)

A simple meme generator exposed as a CLI, web app, and REST API. You can specify an image and a quote (the quote text and author) and you'll get back a meme composed of the quote layered over the image. See below for some sample memes generated from the command line :point_down: :point_down:

![meme sample](./docs/meme-1.jpg "sample meme")
![meme sample](./docs/meme-2.jpg "sample meme")

### Usage:

1.  CLI - generate memes from the command line
    -   clone the [github repo](https://github.com/chalu/turbo-meme-gen)
    -   run `pip install -r requirements.txt` to installs dependencies and setup the environment
    -   run `python3 meme.py` to generate a random meme from our collection of images and quotes. You can also use the `--quotes-dir` and `--images-dir` to specify folders containing your collection of quotes and images to generate a random quote. Finally, you can use the `--count` option to indicate how many memes to randomly generate. See the **How It Works** section for details on how the quotes files are to be structured if you intend to use the `--quotes-dir` option
    -   run `python3 meme.py --qoute "nice quote - author" --img "relative/path/to/img.jpg|jpeg|png|gif"` to generate a meme using the provided image and quote. The `--count` option will be ignored (if used) in this scenario of generating a single meme   

2.  Web App - generate memes on the web
    -   Go to http://url-of-the-app.domain
    -   Click the **Generate** button to see randonly generated memes or use the **Make Yours** form to specify a quote and an image to generate a meme from

3.  REST API
    -   Make a `POST` request to http://url-of-the-app.domain/api with a JSON body containing the quote and image URL like
    ```json
    {
        quote: "some fancy saying - author",
        img: "url-to-the-image-somewhere-online"
    }
    ```

## How It Works

> **Quotes files** are simple files containing a quote per line. A line of quote is a simple text where the **-** character separates the text of the quote from the author. E.g a .txt or .pdf quotes file can have multiple lines like :point_down: :point_down:  <br > `People will never forget how you made them feel - Maya Angelou` <br >  Out of the box, supported quote file formats are .txt, .pdf, .csv, and .docx
---
> **Images** from which to generate the memes can be of any of the popular image formats. So far, we've tested with .jpg | jpeg, and .png

<br >
Under the hood, the system uses a class heirarchy strutured after the strategy design pattern to handle parsing and reading of quotes from files. It then draws a random quote on a random/provided image, which it returns as a meme with a max-height of `500px`

<br >

![quote parsers](./docs/ingestor-strategy.png "quotes parsers")

## Entending It - Adding A Parser/Ingestor for YAML Files

1.  Creat a `YAMLQuotesIngestor` within the `quoteengine` module. It should extend and implement the abstract `QuoteIngestor` class

2.  Add your new parser/ingestor into the `SmartIngestor`
    -   import it, e.g `from .yml_ingestor import YAMLQuotesIngestor as YAMLIngest`
    -   include the imported parser in the returned list in the `ingestors()` method <br>
    ```python
    @classmethod
    def ingestors(cls) -> List[QuoteIngestor]:
        return [..., YAMLIngest]
    ```

3.  Add your YAML quotes file into the `src/_data` folder of the codebase and proceed to generate random memes, which should include quotes from your YAML file. Alternatively, run the meme generator with the `--quotes-dir` option pointing to a directory containing your YAML quotes file

<br>

![custom parser](./docs/custom-parser.png "custom parser")

<br>