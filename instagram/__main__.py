import csv
import logging
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from tqdm import tqdm

from . import Instagram
from .models import MediaType


@dataclass
class Row:
    type: int
    taken_at: int
    code: str
    caption: str
    username: str
    like_count: int


logging.basicConfig(level=logging.DEBUG)

data_path = Path(__file__).parent.parent / 'data'
file_path = data_path / 'instagram' / 'scraped.csv'

with file_path.open('r') as file:
    reader = csv.DictReader(file)
    known_codes = {row['code'] for row in reader}

with file_path.open('a') as file:
    writer = csv.DictWriter(file, fieldnames=[field.name for field in fields(Row)])
    if not file_path.stat().st_size:
        writer.writeheader()

    instagram = Instagram(cookies=Path('data/instagram/cookies.json'))
    for media in tqdm(instagram.iter_media()):
        if media.media_type not in {MediaType.PHOTO, MediaType.SERIES}:
            continue

        if media.code in known_codes:
            continue

        row = Row(
            type=media.media_type.value,
            taken_at=media.taken_at,
            code=media.code,
            caption=media.caption and media.caption.text,
            username=media.user.username,
            like_count=media.like_count,
        )
        writer.writerow(asdict(row))
        file.flush()
