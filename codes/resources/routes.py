from fastapi import APIRouter
from resources import auth, users, feeds, publishers, index

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(feeds.router)
api_router.include_router(publishers.router)
api_router.include_router(index.router)
