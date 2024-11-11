from neomodel import config
import os

class Database:
    def __init__(self):
        config.DATABASE_URL = os.getenv("DB_CONNECT")
