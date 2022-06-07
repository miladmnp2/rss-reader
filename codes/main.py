from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from db import database
from resources.routes import api_router

origins = [
    "http://localhost",
    "http://localhost:4200"
]

app = FastAPI()
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()

    from helpers.users import UserHelper
    import json
    from models.enums import RoleTypes
    from helpers.publishers import PublisherHelper

    if await UserHelper.get_user_by_username('admin'):
        return

    print('Creating admin user')

    token = await UserHelper.register({
        "username": "admin",
        "password": "password",
        "role": RoleTypes.admin.name
    })

    with open("publishers.json", "r") as file_handler:
        publisher_data = json.loads(file_handler.read())
        for publisher in publisher_data:
            await PublisherHelper.add_publisher(publisher)


@app.on_event("startup")
@repeat_every(seconds=3600)
async def run_scraper():
    from helpers.scraper import ScraperHelper
    await ScraperHelper.scrap_publishers_periodically_test()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
