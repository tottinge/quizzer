import json
import os
from typing import NamedTuple, List


class User(NamedTuple):
    user_name: str
    password: str
    role: str

    @staticmethod
    def from_dict(cls, data: dict):
        return cls(**data)


def write_users(user_file_name, users):
    with open(user_file_name, "w") as user_file:
        json.dump(users, user_file)


def read_users(user_file_name: str) -> List[User]:
    try:
        with open(user_file_name) as users_file:
            return json.load(users_file, object_hook=User.from_dict)
    except FileNotFoundError:
        return []


DEFAULT_USER_FILE_PATH = './security/'


def create_user(user_name: str, password: str, role: str,
                user_dir_name: str = DEFAULT_USER_FILE_PATH):
    user_file_name = os.path.join(user_dir_name, USER_FILE_NAME)
    users = read_users(user_file_name)
    exists = any(user for user in users if user.user_name == user_name)
    if not exists:
        new_user = User(user_name=user_name, password=password, role=role)
        users.append(new_user)
    write_users(user_file_name, users)


def find_user_by_name(user_name: str,
                      user_dir_name: str = DEFAULT_USER_FILE_PATH
                      ) -> List[User]:
    user_file_name = os.path.join(user_dir_name, USER_FILE_NAME)
    users = read_users(user_file_name)
    return [profile
            for profile in users
            if profile.user_name == user_name]


USER_FILE_NAME = 'users.json'