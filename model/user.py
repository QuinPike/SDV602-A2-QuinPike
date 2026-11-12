from data.database_manager import DatabaseManager
import bcrypt
import config

class User:

    def __init__(self, name, password, user_id=None):
        self.id = user_id
        self.name = name
        self.password = password