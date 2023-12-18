from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv(".env")

password = os.getenv("MONGO_PASSWORD")
database_name = os.getenv("MONGO_DATABASE")


class Database:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Database, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.client = MongoClient(
            f"mongodb+srv://capstone:{password}@gcp.2boeeer.mongodb.net/?retryWrites=true&w=majority"
        )
        self.db = self.client[database_name]


db = Database().db
