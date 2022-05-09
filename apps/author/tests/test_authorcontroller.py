import tempfile
import unittest
from unittest.mock import Mock, patch

from hamcrest import assert_that, is_, contains_string

from apps.author.author_controller import AuthorController
from quizzes.quiz import Quiz
from quizzes.quiz_file_store import QuizFileStore
from shared.quizzology import Quizzology


class TestAuthorController(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        self.quizzology = Quizzology(
            quiz_store=QuizFileStore(dir_name=self.temp_directory.name)
        )
        self.api = AuthorController(self.quizzology)
        self.quiz = Quiz(name="test quiz", title="New Test Quiz")

    def test_create_new_quiz(self):
        api, quiz = self.api, self.quiz
        result = api.save(quiz)
        assert_that(result.success, is_(True),
                    f"Couldn't save '{quiz.name}': {result.message}")
        assert_that(api.quiz_exists(quiz.name), is_(True),
                    f"Didn't find newly-created '{quiz.name}'")

    def test_save_failure(self):
        api, quiz = self.api, self.quiz
        with patch.object(self.quizzology.quiz_store, "_dump_quiz_to") as fake:
            fake.side_effect = OSError(-1, "fake error")
            result = api.save(quiz)
            assert_that(result.success, is_(False),
                        f"Shouldn't have saved '{quiz.name}'")
            assert_that(api.quiz_exists(quiz.name), is_(False),
                        f"Shouldn't find newly-created '{quiz.name}'")
            assert_that(
                result.message,
                contains_string("fake error"),
                f"Message should contain diagnostic message '{result.message}'"
            )


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
