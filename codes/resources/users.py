from typing import Optional, List

from fastapi import APIRouter, Depends

from helpers.auth import oauth2_scheme, is_admin
from helpers.users import UserHelper
from models import RoleTypes
from schemas.responses.users import UserOut

router = APIRouter(tags=["Users"])


@router.get(
    "/users/users/",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=List[UserOut],
)
async def get_users(username: Optional[str] = None):
    if username:
        return await UserHelper.get_user_by_username(username=username)
    return await UserHelper.get_all_users()


@router.put(
    "/users/{user_id}/make-admin",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_admin(user_id: int):
    await UserHelper.change_role(RoleTypes.admin, user_id)
    return {"success": True}


@router.put(
    "/users/{user_id}/make-scraper",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_scraper(user_id: int):
    await UserHelper.change_role(RoleTypes.scraper, user_id)
    return {"success": True}
