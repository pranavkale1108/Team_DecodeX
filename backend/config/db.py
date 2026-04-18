import os
from pymongo import MongoClient
import pymongo
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "codeatlas"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
repositories_collection = db["repositories"]

# Create unique index on repo_url to ensure uniqueness
repositories_collection.create_index([("repo_url", pymongo.ASCENDING)], unique=True)
