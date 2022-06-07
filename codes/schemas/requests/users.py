from schemas.base import UserBase


class UserRegisterIn(UserBase):
    password: str


class UserLoginIn(UserBase):
    password: str
