from fastapi import APIRouter

from helpers.users import UserHelper
from schemas.requests.users import UserRegisterIn, UserLoginIn

router = APIRouter(tags=["Auth"])


@router.post("/users/register/", status_code=201)
async def register(user_data: UserRegisterIn):
    token = await UserHelper.register(user_data.dict())
    return {"token": token}


@router.post("/users/login/")
async def login(user_data: UserLoginIn):
    token, role = await UserHelper.login(user_data.dict())
    return {"token": token, "role": role}
