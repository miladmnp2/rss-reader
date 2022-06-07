from typing import Optional, List

from fastapi import APIRouter, Depends
from starlette.requests import Request
from helpers.publishers import PublisherHelper
from schemas.requests.publishers import PublisherIn, SubscribeIn
from helpers.auth import oauth2_scheme
from schemas.responses.publishers import PublisherOut

router = APIRouter(tags=["Publishers"])


@router.get("/publishers/publishers/",
            dependencies=[Depends(oauth2_scheme)],
            response_model=List[PublisherOut])
async def get_publishers(publisher_name: Optional[str] = None):
    if publisher_name:
        return await PublisherHelper.get_publisher_by_publisher_name(publisher_name=publisher_name)
    return await PublisherHelper.get_all_publishers()


@router.get("/publishers/subscribed/",
            dependencies=[Depends(oauth2_scheme)],
            response_model=List[PublisherOut])
async def get_user_publishers(request: Request):
    user = request.state.user

    return await PublisherHelper.get_subscribed_publishers(user)


@router.post("/publishers/subscribe/",
             dependencies=[Depends(oauth2_scheme)], status_code=201)
async def subscribe(request: Request, publisher_id: int):
    user = request.state.user

    subscribe_id = await PublisherHelper.subscribe(publisher_id=publisher_id, user=user)

    return {"success": True}
