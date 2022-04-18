import tempfile
import unittest
from unittest.mock import patch

from hamcrest import (assert_that, is_, contains_string, not_)

from quizzes.quiz_store import QuizStore


class TestFilenameGeneration(unittest.TestCase):

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.quiz_store = QuizStore(self.temporary_directory.name)


    def test_adds_json_extension(self):
        assert_that(self.quiz_store.filename_for("poo"), contains_string("poo.json"))

    def test_translates_spaces(self):
        actual = self.quiz_store.filename_for('pooh bear and tigger')
        assert_that(actual, not_(contains_string(' ')))

    def test_handles_path_characters(self):
        actual = self.quiz_store.filename_for('~/c:x/y/blah\this\\')
        end_of_path = len(self.quiz_store.quiz_dir)+1
        actual = actual[end_of_path:]
        for unwanted in '/', '\\', ':', '~':
            assert_that(actual, not_(contains_string(unwanted)))

    def test_handles_scary_bash_characters(self):
        complicated = '\'\" bite me; rm * && rm -rf || format & '
        actual = self.quiz_store.filename_for(complicated)
        for bad_thing in '"\'&|;':
            assert_that(actual, not_(contains_string(bad_thing)))

    def test_does_not_generate_new_filename_for_existing_file(self):
        with patch.object(self.quiz_store, "_find_file_for_named_quiz") as mock:
            existing_path = '/zippidy/doo/dah'
            mock.return_value = existing_path
            assert_that(self.quiz_store.filename_for("whatever"), is_(existing_path))


if __name__ == '__main__':
    unittest.main()
