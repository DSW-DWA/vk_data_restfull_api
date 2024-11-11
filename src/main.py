from fastapi import FastAPI
from vk_api import endpoints
from vk_api.database import Database

db = Database()

app = FastAPI()

app.include_router(endpoints.router)