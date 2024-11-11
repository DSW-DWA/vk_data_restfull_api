from neomodel import config

class Database:
    def __init__(self):
        config.DATABASE_URL = 'bolt://neo4j:12345678@localhost:7687'
