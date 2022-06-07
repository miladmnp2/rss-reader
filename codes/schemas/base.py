from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class PublisherBase(BaseModel):
    name: str


class FeedBase(BaseModel):
    title: str

