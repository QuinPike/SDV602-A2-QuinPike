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
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_collection(self, collection):
        return self.client[config.DB_NAME][collection]

    def insert_one(self, collection, document):
        return self.get_collection(collection).insert_one(document).inserted_id

    def find_one_by_id(self, collection, id):
        return self.get_collection(collection).find_one({"_id": ObjectId(id)})
    
    def find_one_by_name(self, collection, name):
        return self.get_collection(collection).find_one({"name": name})