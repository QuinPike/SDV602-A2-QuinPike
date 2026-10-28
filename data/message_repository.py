from data.database_manager import DatabaseManager
from datetime import datetime
import config

from model.chat_message import ChatMessage

class MessageRepository:
    def __init__(self):
        self.db = DatabaseManager.getInstance()

    def create_message(self, username, text, timestamp=None):
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp


        return self.db.insert_one(config.CHAT_MESSAGES_COLLECTION, {
            "username": username,
            "text": text,
            "timestamp": timestamp
        })

    def all(self):

        collection = self.db.get_collection(config.CHAT_MESSAGES_COLLECTION)

        messages = []

        for document in collection.find().sort("timestamp"):
            message = ChatMessage(document["username"], document["text"], document["timestamp"])
            messages.append(message)

        return messages