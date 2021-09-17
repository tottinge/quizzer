import tempfile
import unittest
from unittest.mock import Mock

from hamcrest import assert_that, is_

from apps.author.author_controller import AuthorController
from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from shared.quizzology import Quizzology


class TestAuthorController(unittest.TestCase):
    def test_create_new_quiz(self):
        with tempfile.TemporaryDirectory() as name:
            quizzology = Quizzology(quiz_store=QuizStore(dir_name=name))
            api = AuthorController(quizzology)
            quiz = Quiz(name="test quiz", title="New Test Quiz")

            result = api.save(quiz)

            assert_that(result.success, is_(True),
                        f"Couldn't save '{quiz.name}': {result.message}")
            assert_that(api.quiz_exists(quiz.name), is_(True),
                        f"Didn't find newly-created '{quiz.name}'")


class LondonSchoolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_store = Mock()
        quizzology = Quizzology(self.mock_store)
        self.api = AuthorController(quizzology)

    def test_create_new_quiz(self):
        quiz = Quiz(name="test quiz", title="New Test Quiz")
        self.api.save(quiz)
        self.mock_store.save_quiz.assert_called_once_with(quiz)

    def test_get_quiz(self):
        self.api.get_quiz("quiz name")
        self.mock_store.get_quiz.assert_called_once_with("quiz name")


if __name__ == '__main__':
    unittest.main()
