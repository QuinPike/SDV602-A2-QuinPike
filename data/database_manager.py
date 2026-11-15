from pymongo import MongoClient
from bson.objectid import ObjectId
import config


class DatabaseManager:

    _instance = None

    def __init__(self):
        self.client = MongoClient(config.MONGO_URI)
        self.client.admin.command("ping")

    @classmethod
    def getInstance(cls):
        """Get the catabase instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_collection(self, collection):
        """Get the database collection"""
        return self.client[config.DB_NAME][collection]

    def insert_one(self, collection, document):
        """Insert into the database"""
        return self.get_collection(collection).insert_one(document).inserted_id

    def find_one_by_id(self, collection, id):
        """Find an item in the database by its ID"""
        return self.get_collection(collection).find_one({"_id": ObjectId(id)})
    
    def find_one_by_name(self, collection, name):
        """Find an item in the database by its name"""
        return self.get_collection(collection).find_one({"name": name})