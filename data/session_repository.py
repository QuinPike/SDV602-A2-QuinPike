from data.database_manager import DatabaseManager
from model.session import Session
from bson import ObjectId

class SessionRepository:

    COLLECTION = "sessions"

    def __init__(self):
        self.db = DatabaseManager.getInstance()
        self.collection = self.db.get_collection(self.COLLECTION)

    def create_session(self, name, creator, is_public=True):
        session = Session(name, creator, is_public)
        return session.save()

    def all(self):
        documents = self.collection.find({
            "is_public": True
        })

        return [
            Session.from_document(document)
            for document in documents
        ]

    def get_session(self, session_id):
        document = self.collection.find_one({
            "_id": ObjectId(session_id)
        })

        if document:
            return Session.from_document(document)

        return None

    def join_session(self, session_id, username):
        result = self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {"$addToSet": {"members": username}}
        )

        return result.matched_count > 0

    def user_sessions(self, username):
        documents = self.collection.find({
            "members": username,
            "is_public": False
        })

        return [
            Session.from_document(document)
            for document in documents
        ]

    def update_graph(self, session_id, graph_settings):
        self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"graph_settings": graph_settings}}
        )

    def get_graph(self, session_id):
        session = self.collection.find_one({
            "_id": ObjectId(session_id)
        })

        if session:
            return session.get("graph_settings")

        return None