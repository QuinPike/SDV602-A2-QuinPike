from data.database_manager import DatabaseManager
import bcrypt
import config

from model.user import User

class UserRepository:
    def __init__(self):
        self.db = DatabaseManager.getInstance()

    def login(self, username, password):
        """Login the user, and if the username or password do not match, then it returns with "invalid password"."""    
        if not type(password) == str or not password:
            raise Exception("Invalid Password")

        try:
            stored_user = self.db.find_one_by_name(config.USER_COLLECTION, username)
            if not stored_user:
                raise Exception("Failed to find user")
            
            password_encoded = password.encode("utf-8")
            result = bcrypt.checkpw(password_encoded, stored_user["password"])

            if not result:
                raise Exception("Failed to login: Incorrect Password")

            return User(username, password)
        except Exception as e:
            print(f"Something went wrong: {e}")
    
    def create_user(self, username, password):
        """Create the user. Also encrypt the password using bcrypt"""
        if self.db.find_one_by_name(config.USER_COLLECTION, username):
            raise Exception("Username already taken")

        password_hash = None
        try:
            password_encoded = password.encode("utf-8")

            # Hash password with bcrypt
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password_encoded, salt)
        except Exception as e:
            print(f"Something went wrong: {e}")

        return self.db.insert_one(config.USER_COLLECTION, {
            "name": username,
            "password": password_hash
        })