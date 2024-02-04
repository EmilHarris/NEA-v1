from menu import Button
import hashlib
import json

try:
    with open('users.json', 'r') as f:
        USERS = json.load(f)

except json.decoder.JSONDecodeError:
    USERS = {}

print(USERS)


class User:
    username: str
    hash_password: hashlib.md5
    high_score: int

    def __init__(self, username, password, highscore=0):
        self.username = username
        self.hash_password = hashlib.md5(password.encode()).hexdigest()
        self.high_score = highscore
        self.save_to_file()

    def save_to_file(self):
        user_dict = {self.username: {'hash_password': self.hash_password, 'high_score': self.high_score}}
        users_dict = USERS | user_dict
        users_obj = json.dumps(users_dict, indent=3)
        with open('users.json', 'w') as f:
            f.writelines(users_obj)
