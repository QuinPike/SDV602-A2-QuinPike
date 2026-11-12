
from data.database_manager import DatabaseManager

""" 
Data repository to help store files inside the database.
"""
class DatasetRepository:

    COLLECTION = "datasets"

    def __init__(self):
        self.db = DatabaseManager.getInstance()

    def create_dataset(self, filename, username, session_id, columns, data):

        document = {
            "filename": filename,
            "uploaded_by": username,
            "session_id": session_id,
            "columns": columns,
            "data": data
        }

        # DatabaseManager.insert_one returns the ObjectId directly
        return self.db.insert_one(self.COLLECTION, document)

    def all_for_session(self, session_id):

        collection = self.db.get_collection(self.COLLECTION)

        datasets = collection.find({"session_id": session_id}).sort("filename", 1)

        return list(datasets)
