from itertools import count
from typing import Iterator

import requests
from anyapi import API

from .models import Explore, Media


class Instagram(API):
    API_URL = 'https://i.instagram.com/api'
    WEB_URL = 'https://www.instagram.com'

    def web_explore(self) -> requests.Response:
        return self.get(f'{self.WEB_URL}/explore/')

    def explore(self, page: int = 0) -> dict:
        return self.get(f'{self.API_URL}/v1/discover/web/explore_grid/', params={
            'is_prefetch': 'false',
            'omit_cover_media': 'false',
            'module': 'explore_popular',
            'use_sectional_payload': 'true',
            'include_fixed_destinations': 'true',
            'max_id': page,
        }).json()

    def iter_explore(self) -> Iterator[Explore]:
        for page in count():
            data = self.explore(page=page)
            yield Explore.parse_obj(data)

    def iter_media(self) -> Iterator[Media]:
        for explore in self.iter_explore():
            for sectional_item in explore.sectional_items:
                layout_content = sectional_item.layout_content
                items = layout_content.one_by_two_item.clips.items + layout_content.fill_items
                yield from (item.media for item in items)
