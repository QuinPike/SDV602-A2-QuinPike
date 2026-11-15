from data.database_manager import DatabaseManager
from model.session import Session
from bson import ObjectId


class SessionRepository:

    COLLECTION = "sessions"

    def __init__(self):
        self.db = DatabaseManager.getInstance()
        self.collection = self.db.get_collection(self.COLLECTION)

    def create_session(self, name, creator, is_public=True):
        """Create a new session, with the name, creator, and if it is public or not"""
        session = Session(name, creator, is_public)
        return session.save()

    def all(self):
        """Find all the sessions that are public"""
        documents = self.collection.find({
            "is_public": True
        })

        return [
            Session.from_document(document)
            for document in documents
        ]

    def get_session(self, session_id):
        """Find a session by its ID"""
        document = self.collection.find_one({
            "_id": ObjectId(session_id)
        })

        if document:
            return Session.from_document(document)

        return None

    def join_session(self, session_id, username):
        """Join a session"""
        result = self.collection.update_one(
            {"_id": ObjectId(session_id)},
            {"$addToSet": {"members": username}}
        )

        return result.matched_count > 0

    def user_sessions(self, username):
        """Get user sessions by their name"""
        documents = self.collection.find({
            "members": username,
            "is_public": False
        })

        return [
            Session.from_document(document)
            for document in documents
        ]

    def initialise_shared_state(self, session_id):
        """Sharing the state with the session, using it's ID. This allows updating a session"""
        session_id = self._get_object_id(session_id)

        self.collection.update_one(
            {
                "_id": session_id,
                "version": {"$exists": False}
            },
            {
                "$set": {
                    "version": 0,
                    "shared_data": [],
                    "shared_columns": []
                }
            }
        )

        self.collection.update_one(
            {
                "_id": session_id,
                "shared_data": {"$exists": False}
            },
            {"$set": {"shared_data": []}}
        )

        self.collection.update_one(
            {
                "_id": session_id,
                "shared_columns": {"$exists": False}
            },
            {"$set": {"shared_columns": []}}
        )

    def get_shared_state(self, session_id):
        """Finding the shared state of a session """

        session_id = self._get_object_id(session_id)

        self.initialise_shared_state(session_id)

        document = self.collection.find_one({
            "_id": session_id
        })

        if not document:
            return None

        return {
            "data": document.get("shared_data", []),
            "columns": document.get("shared_columns", []),
            "graph_settings": document.get("graph_settings"),
            "version": document.get("version", 0)
        }

    def update_shared_state(self, session_id, state, expected_version):
        """Updating a shared state of a session"""

        session_id = self._get_object_id(session_id)

        self.initialise_shared_state(session_id)

        result = self.collection.update_one(
            {
                "_id": session_id,
                "version": expected_version
            },
            {
                "$set": {
                    "shared_data": state["data"],
                    "shared_columns": state["columns"],
                    "graph_settings": state["graph_settings"]
                },
                "$inc": {
                    "version": 1
                }
            }
        )

        if result.matched_count == 0:
            return None

        return expected_version + 1

    def _get_object_id(self, session_id):
        """Finding an object by its ID"""

        if isinstance(session_id, ObjectId):
            return session_id

        return ObjectId(session_id)