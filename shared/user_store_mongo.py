import unittest
from typing import Iterable

from pymongo.collection import Collection

from shared.mongo_connection import db_connection
from shared.user import User
from shared.user_store import UserAlreadyExists

test_connection = db_connection()['test_users']


class UserStoreMongo:
    def __init__(self, collection_name=None):
        self.collection_name = collection_name if collection_name else 'users'

    def create_user(self, user_name: str, password_hash: str, role: str):
        user = User(user_name, password_hash, role)
        criteria = {'user_name': user.user_name}
        with db_connection() as db:
            users: Collection = db.quizzology[self.collection_name]
            if any(users.find(criteria)):
                raise UserAlreadyExists(user.user_name)
            users.insert_one(user._asdict())

    def find_user_by_name(self, user_name: str) -> Iterable[User]:
        exclude_id = {'_id':0}
        criteria = {"user_name": user_name}
        with db_connection() as db:
            users: Collection = db.quizzology[self.collection_name]
            return [
                User.from_dict(json_doc)
                for json_doc in users.find(criteria, projection=exclude_id)
            ]


class TestMongoStore(unittest.TestCase):
    dataset_name = 'test_user_collection'

    def setUp(self):
        self.store = UserStoreMongo(self.dataset_name)

    def tearDown(self):
        with db_connection() as db:
            test_records = db.quizzology[self.dataset_name]
            test_records.drop()

    def test_create_user_works_for_new_user(self):
        self.store.create_user('frank', 'fakehash', 'nobody')
        [result] = self.store.find_user_by_name('frank')
        self.assertEqual('frank', result.user_name)

    def test_cannot_find_nonexistant_user(self):
        self.assertEqual([], self.store.find_user_by_name("nonesuch"))

    def test_cannot_have_two_users_with_same_name(self):
        self.store.create_user('frank', 'beans', 'coleslaw')
        with self.assertRaises(UserAlreadyExists):
            self.store.create_user('frank', 'answers', 'suffice')

    def test_multiple_users_may_exist_with_separate_names(self):
        fred = User('fred', '', '')
        joe = User('joe', '', '')
        self.store.create_user(fred.user_name, fred.password_hash, fred.role)
        self.store.create_user(joe.user_name, joe.password_hash, joe.role)
        with db_connection() as db:
            userbase = db.quizzology[self.dataset_name]
            found = {user['user_name']
                     for user in userbase.find()}
            self.assertEqual(2, len(found))
            self.assertSetEqual(found, {'joe', 'fred'})
