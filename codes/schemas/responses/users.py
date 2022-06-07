from models import RoleTypes
from schemas.base import UserBase


class UserOut(UserBase):
    id: int
    username: str
    role: RoleTypes
