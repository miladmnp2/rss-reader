from typing import Optional

from schemas.base import PublisherBase


class PublisherOut(PublisherBase):
    id: int
    description: Optional[str]
