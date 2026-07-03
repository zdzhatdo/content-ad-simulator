import os
from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_URL = os.environ["REDIS_URL"]

r = redis.from_url(REDIS_URL)