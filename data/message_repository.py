from data.database_manager import DatabaseManager
from datetime import datetime, timezone
import config
import inspect

from model.chat_message import ChatMessage

class MessageRepository:
    def __init__(self):
        self.db = DatabaseManager.getInstance()

    def create_message(self, username, text, session_id):
        message = ChatMessage(
            username,
            text,
            session_id=session_id
        )

        return message.save()
            
    def all(self, session_id):
        collection = self.db.get_collection(config.CHAT_MESSAGES_COLLECTION)

        #Troubleshooting
        print("Database:", config.DB_NAME)
        print("Collection:", config.CHAT_MESSAGES_COLLECTION)
        print("Session ID:", repr(session_id))

        print("Total messages in collection:",
            collection.count_documents({}))

        print("All messages:",
            list(collection.find({})))

        
        documents = collection.find(
            {"session_id": session_id}
        ).sort("timestamp", 1)

        messages = []

        for document in documents:

            message = ChatMessage(
                document["username"],
                document["text"],
                timestamp=document.get("timestamp"),
                session_id=document.get("session_id")
            )

            messages.append(message)

        return messages