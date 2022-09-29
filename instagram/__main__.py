import logging
from itertools import islice
from pathlib import Path

from pprintpp import pprint

from . import Instagram

logging.basicConfig(level=logging.DEBUG)

instagram = Instagram(cookies=Path('data/instagram-cookies.json'))
for media in islice(instagram.iter_media(), 100):
    pprint(media)
