import redis as redis_lib
import dotenv
import os

dotenv.load_dotenv(".env")

REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")


class Redis:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Redis, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        r = redis_lib.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        self.client = r


cache = Redis().client
