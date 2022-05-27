import unittest
from unittest import skip
from unittest.mock import MagicMock, patch

from hamcrest import assert_that, is_

from quizzes.quiz_store_mongo import QuizStoreMongo


class QuizStoreMongoTest(unittest.TestCase):
    @skip("Work In Progress")
    def test_it_retrieves_a_quiz(self):
        test_db_name = "JustTesting"
        store = QuizStoreMongo(test_db_name)
        result = store.get_quiz('fred')
        assert_that(result, is_(None))
        store.db_connection().drop_database(test_db_name)




if __name__ == '__main__':
    unittest.main()

