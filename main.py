from fastapi import FastAPI
from api import endpoints
from database import Database

db = Database()

app = FastAPI()

app.include_router(endpoints.router)