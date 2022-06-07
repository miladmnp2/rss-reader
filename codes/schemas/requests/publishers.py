from pydantic import BaseModel
from schemas.base import PublisherBase
from typing import Optional


class PublisherIn(PublisherBase):
    link: str
    description: Optional[str]


class SubscribeIn(BaseModel):
    user_id: int
    publisher_id: int
