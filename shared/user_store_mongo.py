import unittest
from shared.user import User

from pymongo.collection import Collection
from pymongo.database import Database

from shared.mongo_connection import db_connection

test_connection = db_connection()['test_users']


class UserStoreMongo:
    def __init__(self, collection_name=None):
        self.collection_name = collection_name if collection_name else 'users'

    def create_user(self, user_name: str, password_hash: str, role: str):
        users: Collection
        user = User(user_name, password_hash, role)
        with db_connection() as db:
            users = db.quizzology[self.collection_name]
            users.insert_one(user._asdict())

    def find_user_by_name(self, user_name: str):
        users: Collection
        with db_connection() as db:
            users = db.quizzology[self.collection_name]
            user = users.find({"user_name": user_name})
            return user


class TestMongoStore(unittest.TestCase):
    dataset_name = 'test_collection_only'

    def setUp(self):
        self.store = UserStoreMongo(self.dataset_name)

    def tearDown(self):
        db: Database = db_connection().quizzology
        test_records = db[self.dataset_name]
        test_records.drop()

    def test_create_user_works_for_new_user(self):
        frank = self.store.create_user('frank', 'fakehash', 'nobody')
        print(frank)
        result = self.store.find_user_by_name('frank')
        print(result)

        # store.create_user('notreal', 'fakehash', 'imaginaryfriend')
