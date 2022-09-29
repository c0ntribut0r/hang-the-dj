from pydantic import Extra
from pydantic import BaseModel


class Media(BaseModel):
    taken_at: int
    pk: str
    id: str
    code: str
    caption: dict | None

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


class LayoutContent(BaseModel):
    one_by_two_item: OneByTwoItem
    fill_items: list[Item]

    class Config:
        extra = Extra.ignore


class SectionalItem(BaseModel):
    layout_content: LayoutContent

    class Config:
        extra = Extra.ignore


class Explore(BaseModel):
    sectional_items: list[SectionalItem]

    class Config:
        extra = Extra.ignore
