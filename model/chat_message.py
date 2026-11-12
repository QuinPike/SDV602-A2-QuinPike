from data.database_manager import DatabaseManager

class ChatMessage:
    # Make a collection variable 
    COLLECTION = "messages"

    def __init__(self, username, text, timestamp=None, session_id=None):
        self.username = username
        self.text = text
        self.timestamp = timestamp
        self.session_id = session_id

    def save(self):
        db = DatabaseManager.getInstance()

        document = {
            "username": self.username,
            "text": self.text,
            "timestamp": self.timestamp,
            "session_id": self.session_id
        }

        db.insert_one(self.COLLECTION, document)

    @classmethod
    def all(cls, session_id):
        db = DatabaseManager.getInstance()
        
        collection = db.get_collection(cls.COLLECTION)

        documents = collection.find().sort("_id", 1)

        messages = []

        for document in documents:
            message = cls(
                username=document["username"],
                text=document["text"],
                timestamp=document.get("timestamp"),
                session_id=document.get("session_id")
            )
            messages.append(message)

        return messages