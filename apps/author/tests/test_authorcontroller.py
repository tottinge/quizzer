import tempfile
import unittest

from hamcrest import assert_that, is_

from apps.author.author_controller import AuthorController
from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from shared.quizzology import Quizzology


class TestAuthorController(unittest.TestCase):
    def test_create_new_quiz(self):
        with tempfile.TemporaryDirectory() as name:
            quiz_store = QuizStore(dir_name=name)
            quizzology = Quizzology(quiz_store=quiz_store)
            api = AuthorController(quizzology)
            quiz = Quiz(name="test quiz", title="New Test Quiz")
            result = api.save(quiz)
            assert_that(result.success, is_(True))


if __name__ == '__main__':
    unittest.main()
