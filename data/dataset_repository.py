from data.database_manager import DatabaseManager
from bson import ObjectId

"""
Data repository to help store files inside the database.
"""
class DatasetRepository:

    COLLECTION = "datasets"

    def __init__(self):
        self.db = DatabaseManager.getInstance()

    def create_dataset(self, filename, username, session_id, columns, data):
        """Create a new dataset with its name, the username that it was uploaded by, the session ID that it is in, the columns, and it's data"""

        document = {
            "filename": filename,
            "uploaded_by": username,
            "session_id": session_id,
            "columns": columns,
            "data": data
        }

        return self.db.insert_one(self.COLLECTION, document)

    def all_for_session(self, session_id):
        """Find the datasets for the session"""

        collection = self.db.get_collection(self.COLLECTION)

        datasets = collection.find(
            {"session_id": session_id}
        ).sort("filename", 1)

        return list(datasets)

    def get_by_id(self, dataset_id, session_id):
        """Find the dataset by its ID"""

        collection = self.db.get_collection(self.COLLECTION)

        return collection.find_one({
            "_id": ObjectId(dataset_id),
            "session_id": session_id
        })

    def update_dataset(self, dataset_id, session_id, columns, data):
        """Update the dataset"""

        collection = self.db.get_collection(self.COLLECTION)

        return collection.update_one(
            {
                "_id": ObjectId(dataset_id),
                "session_id": session_id
            },
            {
                "$set": {
                    "columns": columns,
                    "data": data
                }
            }
        )        