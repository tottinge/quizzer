import unittest
from json import JSONDecodeError
from unittest.mock import patch, mock_open, MagicMock

from hamcrest import assert_that, is_

from quizzes.quiz_store import QuizStore, logger, QuizSummary


class QuizStoreTest(unittest.TestCase):
    @patch('os.listdir', return_value=['a.json'])
    @patch('builtins.open')
    @patch('json.load', return_value=dict(name="name", title="a title"))
    def test_it_gets_a_summary_of_test(self, *_):
        store = QuizStore()
        expected = {QuizSummary('name', 'a title', 'quiz_content/a.json')}
        actual = set(store.get_quiz_summaries())
        assert_that(actual, is_(expected))

    def test_it_retrieves_a_quiz(self, *_):
        store = QuizStore()
        test_quiz = 'Testquiz'
        store.get_quiz_summaries = MagicMock(return_value=[
            QuizSummary('Testquiz', '', 'quiz_content/a.json')
        ])
        store._read_quiz_doc_from_file = MagicMock(
            return_value=dict(name='Testquiz')
        )

        actual = store.get_quiz(test_quiz)

        assert_that(actual.name, is_(test_quiz))

    @patch('os.listdir', side_effect=FileNotFoundError('boo'))
    def test_returns_empty_list_and_log_exception_if_no_quiz_dir(self, _):
        store = QuizStore()
        store.quiz_dir = 'nonesuch_directory_exists_here'
        with patch.object(logger, 'error'):
            returned_summaries = list(store.get_quiz_summaries())
            self.assertEqual([], returned_summaries)
            logger.error.assert_called_with("Reading quiz directory: boo")

    @patch('builtins.open')
    @patch('json.load', side_effect=JSONDecodeError('yuck', 'testfile', 0))
    def test_json_file_invalid(self, *_):
        store = QuizStore()
        store.get_quiz_summaries = MagicMock(return_value=[
            QuizSummary('nonesuch', 'no title', 'nonesuch.json'),
        ])
        quiz = store.get_quiz('nonesuch')
        assert_that(quiz, is_(None))

    def test_get_a_list_of_test_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.json']):
            expected = ["q/a.json", "q/b.json"]
            store = QuizStore()
            actual = sorted(store._get_quiz_files_from_directory("q"))
            assert_that(actual, is_(expected))

    def test_get_test_files_ignores_non_json_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.txt']):
            expected = {"q/a.json"}
            store = QuizStore()
            assert_that(
                set(store._get_quiz_files_from_directory("q")),
                is_(expected)
            )

    def test_get_summary_handles_empty_lists(self):
        store = QuizStore()
        actual = store._get_quiz_summaries_from_file_list([])
        assert_that(list(actual), is_([]))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_one_summary(self):
        store = QuizStore()
        json_for_file = dict(name='pass', title='a test that passes')
        with patch('json.load', return_value=json_for_file):
            expected = [
                QuizSummary('pass', 'a test that passes', 'd/pass.json')]
            actual = store._get_quiz_summaries_from_file_list(['d/pass.json'])
            assert_that(list(actual), is_(expected))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_multiple_summary(self):
        store = QuizStore()
        expected = [
            QuizSummary('cats', 'a tests about felines', 'd/cats.json'),
            QuizSummary('dogs', 'explore the canine world', 'd/dogs.json')
        ]
        filenames = [path for (_, _, path) in expected]
        json_docs = [dict(name=name, title=title)
                     for (name, title, _) in expected]
        with patch("json.load", side_effect=json_docs):
            actual = store._get_quiz_summaries_from_file_list(filenames)
            assert_that(list(actual), is_(expected))

    # Test for empty quiz list
    # Test for no questions in file


if __name__ == '__main__':
    unittest.main()
