from enum import Enum
from typing import Iterator

from pydantic import BaseModel, Extra, ValidationError, root_validator


class Caption(BaseModel):
    text: str

    class Config:
        extra = Extra.ignore


class User(BaseModel):
    pk: int
    username: str

    class Config:
        extra = Extra.ignore


class MediaType(Enum):
    PHOTO = 1
    VIDEO = 2
    SERIES = 8


class Media(BaseModel):
    taken_at: int
    media_type: MediaType
    pk: str
    id: str
    code: str
    caption: Caption | None
    user: User
    like_count: int

    class Config:
        extra = Extra.ignore


class Item(BaseModel):
    media: Media

    class Config:
        extra = Extra.ignore


class Clips(BaseModel):
    items: list[Item]

    class Config:
        extra = Extra.ignore


class OneByTwoItem(BaseModel):
    clips: Clips

    class Config:
        extra = Extra.ignore


class OneByTwoLayoutContent(BaseModel):
    one_by_two_item: OneByTwoItem
    fill_items: list[Item]

    class Config:
        extra = Extra.ignore

    def iter_media(self) -> Iterator[Media]:
        yield from (item.media for item in self.one_by_two_item.clips.items)
        yield from (item.media for item in self.fill_items)


class MediaGridLayoutContent(BaseModel):
    medias: list[Item]

    class Config:
        extra = Extra.ignore

    def iter_media(self) -> Iterator[Media]:
        yield from (item.media for item in self.medias)


class LayoutType(Enum):
    ONE_BY_TWO_LEFT = 'one_by_two_left'
    ONE_BY_TWO_RIGHT = 'one_by_two_right'
    MEDIA_GRID = 'media_grid'


class SectionalItem(BaseModel):
    layout_type: LayoutType
    layout_content: OneByTwoLayoutContent | MediaGridLayoutContent

    class Config:
        extra = Extra.ignore

    @root_validator
    def check_fields(cls, values):
        match values['layout_type']:
            case LayoutType.ONE_BY_TWO_LEFT | LayoutType.ONE_BY_TWO_RIGHT:
                assert isinstance(values['layout_content'], OneByTwoLayoutContent)
            case LayoutType.MEDIA_GRID:
                assert isinstance(values['layout_content'], MediaGridLayoutContent)
            case _:
                raise ValidationError('Unsupported layout type')

        return values


class Explore(BaseModel):
    sectional_items: list[SectionalItem]

    class Config:
        extra = Extra.ignore
