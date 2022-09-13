import unittest
from os import environ
from unittest import skipIf

from apps.study.session_store_mongodb import SessionStoreMongoDB
from shared.mongo_connection import db_connection


@skipIf(environ.get("QUIZ_MONGO_URL") is None, "MongoDB not in use")
class MyTestCase(unittest.TestCase):
    dataset_name = 'test_user_session'

    def setUp(self):
        self.store = SessionStoreMongoDB(self.dataset_name)

    def tearDown(self):
        with db_connection() as db:
            test_records = db.quizzology[self.dataset_name]
            test_records.drop()

    def test_record_answer(self):
        result: bool = self.store.record_answer(
            'session_uuid',
            'fake_quiz',
            0,
            'no real answer',
            True,
            'question_uuid'
        )
        self.assertTrue(result)
