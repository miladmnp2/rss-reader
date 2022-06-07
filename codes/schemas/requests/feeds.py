from typing import Optional
from pydantic import BaseModel

from schemas.base import FeedBase


class FeedIn(FeedBase):
    link: Optional[str]
    description: Optional[str]
    publisher_id: int


class FavouriteIn(BaseModel):
    user_id: int
    feed_id: int


class CommentIn(BaseModel):
    feed_id: int
    text: str
