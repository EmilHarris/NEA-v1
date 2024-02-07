# Imports

import hashlib
import json

# Import USERS dict from file

USERS = {}

try:
    with open('users.json', 'r') as f:
        USERS = json.load(f)

except json.decoder.JSONDecodeError:
    USERS = {}


# User class is used to manage attributes of a user
class User:
    username: str
    hash_password: hashlib.md5
    high_score: int

    # constructor method sets attributes
    def __init__(self, username, password, highscore=0):
        self.username = username

        # Uses md5 hash to store password securely
        self.hash_password = hashlib.md5(password.encode()).hexdigest()

        self.high_score = highscore

    # Returns a dictionary of the users attributes
    def get_dict(self):
        return {self.username: {'hash_password': self.hash_password, 'high_score': self.high_score}}

    # updates teh dict for all users and saves to file
    def save_to_file(self):
        user_dict = {self.username: {'hash_password': self.hash_password, 'high_score': self.high_score}}
        users_dict = USERS | user_dict
        users_obj = json.dumps(users_dict, indent=3)
        with open('users.json', 'w') as f:
            f.writelines(users_obj)
