import unittest
from os import environ
from unittest import skipIf

from apps.study.session_store_mongodb import SessionStoreMongoDB
from shared.mongo_connection import db_connection


@skipIf(environ.get("QUIZ_MONGO_URL") is None, "MongoDB not in use")
class MongoSessionStoreTest(unittest.TestCase):
    dataset_name = "test_user_session"

    def setUp(self):
        self.store = SessionStoreMongoDB(self.dataset_name)

    def tearDown(self):
        with db_connection() as db:
            test_records = db.quizzology[self.dataset_name]
            test_records.drop()

    def test_record_answer(self):
        session_uuid = "session_uuid"
        quiz_name = "fake_quiz"
        question_number = 0
        selection = "no real answer"
        is_correct = True
        question_id = "question_uuid"
        result: bool = self.store.record_answer(
            session_uuid, quiz_name, question_number, selection, is_correct, question_id
        )
        self.assertTrue(result)
        self.record = self.store.get_log_message(
            session_uuid, quiz_name, question_number
        )
        # Todo - Finish implementing assert with the get_log_message result
