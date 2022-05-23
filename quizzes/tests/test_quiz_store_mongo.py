import unittest

from quizzes.quiz_store_mongo import QuizStoreMongo


class QuizStoreMongoTest(unittest.TestCase):
    def test_it_retrieves_a_quiz(self):
        store = QuizStoreMongo()

        # self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()

