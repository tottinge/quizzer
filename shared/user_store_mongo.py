from dataclasses import asdict

from pymongo.collection import Collection

from shared.mongo_connection import db_connection
from shared.user import User


def get_collection() -> Collection:
    return db_connection()['users']


class UserStoreMongo:

    def create_user(self, user_name: str, password_hash: str, role: str):
        users: Collection
        user = User(user_name, password_hash, role)
        with get_collection() as users:
            users.insert_one(user._asdict())

    def find_user_by_name(self, user_name):
        with get_collection() as users:
            user = users.find({"user_name": user_name})
            return user
        # ToDo:  Should this return a user object or a list of Profiles
