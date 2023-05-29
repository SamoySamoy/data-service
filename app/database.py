from pymongo import mongo_client
import pymongo
from app.config import settings

client = mongo_client.MongoClient(settings.DATABASE_URL)
print("Connecting to MongoDB...")

db = client[settings.MONGO_INITDB_DATABASE]
User = db.users
Holiday = db.holidays
Stock = db.stocks
User.create_index([("email", pymongo.ASCENDING)], unique=True)
Holiday.create_index([("date", pymongo.ASCENDING)], unique=True)
Stock.create_index([("name", pymongo.ASCENDING)], unique=True)
