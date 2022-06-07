from typing import Optional, List

from fastapi import APIRouter, Depends

from helpers.auth import oauth2_scheme
from helpers.feeds import FeedHelper
from starlette.requests import Request

from schemas.responses.feeds import FeedOut, CommentOut

router = APIRouter(tags=["Index"])


@router.get(
    "/"
)
async def index():
    return {"name": "RSS Reader",
            "Docs": "{base_url}/docs"}
