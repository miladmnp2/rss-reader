from fastapi import HTTPException
from asyncpg import UniqueViolationError
from db import database
from models import subscribers, publishers


class PublisherHelper:
    @staticmethod
    async def get_all_publishers():
        return await database.fetch_all(publishers.select())

    @staticmethod
    async def get_publisher_by_publisher_name(publisher_name: str):
        return await database.fetch_all(publishers.select().where(publishers.c.name == publisher_name))

    @staticmethod
    async def get_subscribed_publishers(user):
        return await database.fetch_all(publishers.select().join(
            subscribers, subscribers.c.publisher_id == publishers.c.id).where(
            subscribers.c.user_id == user["id"]))

    @staticmethod
    async def subscribe(user, publisher_id):
        data = {"user_id": user["id"], "publisher_id": publisher_id}
        return await database.execute(subscribers.insert().values(**data))

    @staticmethod
    async def add_publisher(publisher_date):
        try:
            id_ = await database.execute(publishers.insert().values(**publisher_date))
        except UniqueViolationError:
            raise HTTPException(400, "Publisher with this name already exists")
        return id_
