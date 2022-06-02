import os
import unittest
from unittest import skip, skipIf
from unittest.mock import MagicMock, patch

from hamcrest import assert_that, is_

from quizzes.quiz import Quiz
from quizzes.quiz_store_mongo import QuizStoreMongo


class QuizStoreMongoTest(unittest.TestCase):
    @skipIf(os.environ.get("QUIZ_MONGO_URL", None) is None, "No database configured")
    def test_it_retrieves_a_quiz(self):
        test_db_name = "JustTesting"
        store = QuizStoreMongo(test_db_name)
        store.save_quiz(Quiz("fred","What we said",[]))
        result = store.get_quiz('fred')
        assert_that(result["name"], is_("fred"))
        assert_that(result["title"], is_("What we said"))
        # ToDo: Figure out how to get permission to drop a database
        # store.db_connection().drop_database(test_db_name)





if __name__ == '__main__':
    unittest.main()

