import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

DB_NAME = "practice2"
DATA_SOURCES_COLLECTION = "data_sources"
CHAT_MESSAGES_COLLECTION = "chat_messages"

POLL_RATE=1000