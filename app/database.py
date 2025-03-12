from pymongo import MongoClient
from app.config import settings

client = MongoClient(settings.MONGO_URI)
db = client["chatbot"]

users_collection = db["users"]
chats_collection = db["chats"]
