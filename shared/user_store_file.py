import json
import os
from typing import Iterable, List

from shared.user import User, hash_password
from shared.user_store import UserAlreadyExists

USER_FILE_NAME = 'users.json'
DEFAULT_USER_FILE_PATH = './security/'


class UserStore_File:
    path = DEFAULT_USER_FILE_PATH
    user_file_name: str

    def __init__(self, alternate_file_path=None):
        self.path = alternate_file_path or DEFAULT_USER_FILE_PATH
        self.user_file_name = os.path.join(self.path, USER_FILE_NAME)

    def write_users(self, users: Iterable[User], ):
        with open(self.user_file_name, "w") as user_file:
            json.dump([user._asdict() for user in users], user_file)

    def read_users(self) -> List[User]:
        try:
            with open(self.user_file_name) as users_file:
                return json.load(users_file, object_hook=User.from_dict)
        except FileNotFoundError:
            return []

    def create_user(self, user_name: str, password: str, role: str):
        users = self.read_users()
        if any(user for user in users if user.user_name == user_name):
            raise UserAlreadyExists()
        password_hash = hash_password(password)
        new_user = User(
            user_name=user_name,
            password_hash=password_hash,
            role=role
        )
        users.append(new_user)
        self.write_users(users)

    def find_user_by_name(self, user_name) -> Iterable[User]:
        user_list = self.read_users()
        return [profile
                for profile in user_list
                if profile.user_name == user_name]
