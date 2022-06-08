import os
import unittest
from unittest import skipIf

from hamcrest import assert_that, is_

from quizzes.quiz import Quiz
from quizzes.quiz_store_mongo import QuizStoreMongo, db_connection


@skipIf(os.environ.get("QUIZ_MONGO_URL", None) is None,
        "No database configured")
class QuizStoreMongoTest(unittest.TestCase):
    temporary_data_set = "test_quiz_store"

    def setUp(self) -> None:
        self.store = QuizStoreMongo(self.temporary_data_set)

    def tearDown(self) -> None:
        with db_connection() as db:
            result = db.quizzology.drop_collection(self.temporary_data_set)
            assert_that(result['ok'], is_(True))


    def test_it_creates_and_retrieves_a_simple_quiz(self):
        store = self.store
        store.save_quiz(Quiz("fred", "What we said", []))
        result = store.get_quiz('fred')
        assert_that(result.name, is_("fred"))
        assert_that(result.title, is_("What we said"))

    def test_updates_exist_quiz_if_name_exists(self):
        store = self.store
        original = Quiz("uniquename", "first attempt", [])
        revised = Quiz("uniquename", "revision", [])
        store.save_quiz(original)
        store.save_quiz(revised)
        item = store.get_quiz('uniquename')
        assert_that(item.title, is_(revised.title))

    #TODO: GetQuizSummaries needs a test and implemenation

if __name__ == '__main__':
    unittest.main()
