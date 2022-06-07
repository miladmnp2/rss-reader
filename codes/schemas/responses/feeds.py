from schemas.base import FeedBase
from pydantic import BaseModel
from datetime import datetime


class FeedOut(FeedBase):
    id: int
    link: str
    created_at: datetime


class CommentOut(BaseModel):
    id: int
    text: str
    username: str


class FullFeedOut(FeedOut):
    description: str
