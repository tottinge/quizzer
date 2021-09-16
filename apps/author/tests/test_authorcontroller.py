import tempfile
import unittest
from unittest.mock import Mock

from hamcrest import assert_that, is_

from apps.author.author_controller import AuthorController
from quizzes.quiz import Quiz
from quizzes.quiz_store import QuizStore
from shared.quizzology import Quizzology


class TestAuthorController(unittest.TestCase):
    def test_create_new_quiz_chicagoSchool(self):
        with tempfile.TemporaryDirectory() as name:
            quizzology = Quizzology(quiz_store=QuizStore(dir_name=name))
            api = AuthorController(quizzology)
            quiz = Quiz(name="test quiz", title="New Test Quiz")

            result = api.save(quiz)

            assert_that(result.success, is_(True),
                        f"Couldn't save '{quiz.name}': {result.message}")
            assert_that(api.quiz_exists(quiz.name), is_(True),
                        f"Didn't find newly-created '{quiz.name}'")

    def test_create_new_quiz_londonSchool(self):
        mock_store = Mock()
        quizzology = Quizzology(mock_store)
        api = AuthorController(quizzology)
        quiz = Quiz(name="test quiz", title="New Test Quiz")

        api.save(quiz)

        mock_store.save_quiz.assert_called_once_with(quiz)

        

if __name__ == '__main__':
    unittest.main()
