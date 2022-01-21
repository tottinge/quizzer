import json
import logging
import os
from typing import NamedTuple, List, Iterable, Optional


class User(NamedTuple):
    user_name: str
    password: str
    role: str

    @classmethod
    def from_dict(cls, data: dict):
        logging.info(f"cls is {cls}")
        return cls(**data)


DEFAULT_USER_FILE_PATH = './security/'
USER_FILE_NAME = 'users.json'


class UserDatabase:
    path = DEFAULT_USER_FILE_PATH
    user_file_name: str

    def __init__(self, alternate_file_path=None):
        self.path = alternate_file_path or DEFAULT_USER_FILE_PATH
        self.user_file_name = os.path.join(self.path, USER_FILE_NAME)

    def write_users(self, users, alternate_file_path=None):
        chosen = alternate_file_path or self.path
        with open(chosen, "w") as user_file:
            json.dump(users, user_file)

    def read_users(self, user_file_name: str = None) -> List[User]:
        chosen = user_file_name or self.user_file_name
        try:
            with open(chosen) as users_file:
                return json.load(users_file, object_hook=User.from_dict)
        except FileNotFoundError:
            return []

    def create_user(self, user_name: str, password: str, role: str,
                    user_dir_name: Optional[str] = None):
        if user_dir_name:
            user_file_name = os.path.join(user_dir_name, USER_FILE_NAME)
        else:
            user_file_name = self.user_file_name
        users = read_users(user_file_name)
        exists = any(user for user in users if user.user_name == user_name)
        if not exists:
            new_user = User(user_name=user_name, password=password, role=role)
            users.append(new_user._asdict())
        write_users(user_file_name, users)

    def find_user_by_name(self, user_name):
        user_list = self.read_users()
        return [ profile
                 for profile in user_list
                 if profile.user_name == user_name ]


def write_users(user_file_name, users: Iterable[User]):
    db = UserDatabase()
    db.write_users(users, user_file_name)

def read_users(user_file_name: str = None) -> List[User]:
    db = UserDatabase()
    return db.read_users(user_file_name)

def create_user(user_name: str, password: str, role: str,
                user_dir_name: str = DEFAULT_USER_FILE_PATH):
    db = UserDatabase(user_dir_name)
    db.create_user(user_name, password, role)


def find_user_by_name(user_name: str,
                      user_dir_name: str = DEFAULT_USER_FILE_PATH
                      ) -> List[User]:
    db = UserDatabase(user_dir_name)
    return db.find_user_by_name(user_name)
