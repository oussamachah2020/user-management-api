from pymongo import MongoClient
from .settings import settings

client = MongoClient(settings.MONGO_URI)
db = client["user-data"]
