from menu import Button
import json

try:
    with open('users.json', 'r') as f:
        USERS = json.load(f)

except json.decoder.JSONDecodeError:
    USERS = {}


class User:
    username: str
    hash_password: int
    high_score: int

    def __init__(self, username, password):
        self.username = username
        self.hash_password = hash(password)
        self.high_score = 0
        self.save_to_file()

    def save_to_file(self):
        with open('users.json', 'w') as f:
            info = USERS|{self.username: [self.hash_password, self.high_score]}
            line = json.dumps(info)
            f.writelines(line)