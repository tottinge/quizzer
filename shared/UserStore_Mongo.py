from typing import Iterable

from shared.mongo_connection import db_connection
from shared.user import User


class UserStore_Mongo:
    def _get_collection(self):
        return db_connection()['users']

    def write_users(self, users: Iterable[User]):
        with self._get_collection() as db:
            ...

    def read_users(self, users: Iterable[User]):
        ...

    def create_user(self, user_name: str, password: str, role: str):
        ...

    def find_user_by_name(self, user_name):
        ...
