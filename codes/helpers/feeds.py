from fastapi import HTTPException
from db import database
from asyncpg import UniqueViolationError
from models import feeds, subscribers, publishers, RoleTypes, favourites, comments, seen, users
import sqlalchemy as sa
from sqlalchemy import desc


class FeedHelper:
    @staticmethod
    async def get_feeds(user):
        if user["role"] in [RoleTypes.reader]:
            # ToDo: Apply seen
            return await database.fetch_all(
                sa.select([feeds]).join(
                    publishers, publishers.c.id == feeds.c.publisher_id).join(
                    subscribers, subscribers.c.publisher_id == publishers.c.id).where((
                        subscribers.c.user_id == user["id"])).where(
                    feeds.c.id.notin_(sa.select(seen.c.feed_id).where(
                        seen.c.user_id == user["id"]))).order_by(desc(feeds.c.created_at)))

        elif user["role"] in [RoleTypes.admin]:
            return await database.fetch_all(sa.select([feeds]).order_by(desc(feeds.c.created_at)))
        else:
            raise HTTPException(403, "Forbidden")

    @staticmethod
    async def create_feed(feed_data: dict):
        try:
            id_ = await database.execute(feeds.insert().values(**feed_data))
        except UniqueViolationError:
            print("Not unique feed crawled")

    @staticmethod
    async def get_feed_comments(feed_id: int):
        return await database.fetch_all(
            sa.select([comments.c.id, comments.c.text, users.c.username]).join(
                users, users.c.id == comments.c.user_id).where(
                comments.c.feed_id == feed_id))

    @staticmethod
    async def get_seen_feeds(user):
        return await database.fetch_all(
            feeds.select().join(
                seen, seen.c.feed_id == feeds.c.id).where(seen.c.user_id == user["id"]))

    @staticmethod
    async def get_favorite_feeds(user):
        return await database.fetch_all(
            feeds.select().join(
                favourites, favourites.c.feed_id == feeds.c.id).where(favourites.c.user_id == user["id"]))

    @staticmethod
    async def get_publisher_feeds(publisher_id):
        return await database.fetch_all(
            feeds.select().where(feeds.c.publisher_id == publisher_id))

    @staticmethod
    async def fave(feed_id, user):
        data = {"user_id": user["id"], "feed_id": feed_id}
        return await database.execute(favourites.insert().values(**data))

    @staticmethod
    async def fave_undo(feed_id, user):
        await database.execute(
            favourites.delete().where(
                favourites.c.user_id == user["id"], favourites.c.feed_id == feed_id))

    @staticmethod
    async def add_comment(user, comment_data):
        comment_data["user_id"] = user["id"]
        return await database.execute(comments.insert().values(**comment_data))

    @staticmethod
    async def remove_comment(comment_id, user):
        await database.execute(
            comments.delete().where(
                comments.c.user_id == user["id"], comments.c.id == comment_id))

    @staticmethod
    async def view(user, feed_id):
        data = {"user_id": user["id"], "feed_id": feed_id}
        return await database.execute(seen.insert().values(**data))
