from fastapi import HTTPException
from passlib.context import CryptContext
from asyncpg import UniqueViolationError, NoDataFoundError, CaseNotFoundError
from db import database
from helpers.auth import AuthenticationHelper
from models import users, RoleTypes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserHelper:
    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(users.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this username already exists")
        user_do = await database.fetch_one(users.select().where(users.c.id == id_))
        return AuthenticationHelper.encode_token(user_do)

    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(
            users.select().where(users.c.username == user_data["username"])
        )
        if not user_do:
            raise HTTPException(400, "Wrong username or password")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong username or password")
        return AuthenticationHelper.encode_token(user_do), user_do["role"]

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(users.select())

    @staticmethod
    async def get_user_by_username(username):
        return await database.fetch_all(users.select().where(users.c.username == username))

    @staticmethod
    async def change_role(role: RoleTypes, user_id):
        await database.execute(
            users.update().where(users.c.id == user_id).values(role=role.name)
        )
