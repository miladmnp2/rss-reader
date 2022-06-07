from typing import Optional, List

from fastapi import APIRouter, Depends

from helpers.auth import oauth2_scheme
from helpers.feeds import FeedHelper
from starlette.requests import Request

from schemas.responses.feeds import FeedOut, CommentOut
from schemas.requests.feeds import CommentIn

router = APIRouter(tags=["Feeds"])


@router.get(
    "/feeds/feeds/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[FeedOut],
)
async def get_feeds(request: Request, publisher_id: Optional[int] = None):
    user = request.state.user
    if publisher_id:
        return await FeedHelper.get_publisher_feeds(publisher_id=publisher_id)
    return await FeedHelper.get_feeds(user=user)


@router.get(
    "/feeds/liked/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[FeedOut],
)
async def get_favorites(request: Request):
    user = request.state.user
    return await FeedHelper.get_favorite_feeds(user=user)


@router.post(
    "/feeds/like/",
    dependencies=[Depends(oauth2_scheme)]
)
async def like(request: Request, feed_id: int):
    user = request.state.user
    _ = await FeedHelper.fave(feed_id=feed_id, user=user)
    return {"success": True}


@router.delete(
    "/feeds/unlike/",
    dependencies=[Depends(oauth2_scheme)],
)
async def unlike(request: Request, feed_id: int):
    user = request.state.user
    _ = await FeedHelper.fave_undo(feed_id=feed_id, user=user)
    return {"success": True}


@router.get(
    "/feeds/comments/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[CommentOut],
)
async def get_commented(feed_id: int):
    return await FeedHelper.get_feed_comments(feed_id=feed_id)


@router.post(
    "/feeds/comments/",
    dependencies=[Depends(oauth2_scheme)]
)
async def comment(request: Request, comment_data: CommentIn):
    user = request.state.user
    _ = await FeedHelper.add_comment(user=user, comment_data=comment_data.dict())
    return {"success": True}


@router.delete(
    "/feeds/uncomment/",
    dependencies=[Depends(oauth2_scheme)],
)
async def uncomment(request: Request, comment_id: int):
    user = request.state.user
    _ = await FeedHelper.remove_comment(comment_id=comment_id, user=user)
    return {"success": True}


@router.post(
    "/feeds/view/",
    dependencies=[Depends(oauth2_scheme)]
)
async def viewed(request: Request, feed_id: int):
    user = request.state.user
    _ = await FeedHelper.view(user=user, feed_id=feed_id)
    return {"success": True}


@router.get(
    "/feeds/seen/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[FeedOut],
)
async def get_seen(request: Request):
    user = request.state.user
    return await FeedHelper.get_seen_feeds(user=user)
