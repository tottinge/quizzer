import unittest
from json import JSONDecodeError
from unittest.mock import patch, mock_open

import hamcrest
from hamcrest import assert_that, contains_inanyorder, is_

from quizzes.quiz_store import QuizStore, logger


class QuizStoreTest(unittest.TestCase):
    @patch('os.listdir', return_value=['a.json'])
    @patch('builtins.open')
    @patch('json.load', return_value=dict(name="name", title="a title"))
    def test_it_gets_a_summary_of_test(self, *_):
        store = QuizStore()
        expected = {('name', 'a title', 'quiz_content/a.json')}
        actual = set(store.get_quiz_summaries())
        assert_that(actual, is_(expected))

    @patch('main.QuizStore.get_quiz_summaries', return_value=[
        ('Testquiz', None, 'quiz_content/a.json')
    ])
    @patch('main.QuizStore._read_quiz_doc_from_file',
           return_value=dict(name='Testquiz'))
    def test_it_retrieves_a_quiz(self, *_):
        store = QuizStore()
        test_quiz = 'Testquiz'
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

    @patch('main.QuizStore.get_quiz_summaries')
    @patch('builtins.open')
    @patch('json.load', side_effect=JSONDecodeError('yuck', 'testfile', 0))
    # ToDo: this test needs a rewrite.
    def test_json_file_invalid(self, summaries_mock, *_):
        summaries_mock.return_value = [
            ('nonesuch', 'no title', 'nonesuch.json'), ]
        store = QuizStore()
        store.get_quiz('nonesuch')

    def test_get_a_list_of_test_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.json']):
            expected = "q/a.json", "q/b.json"
            store = QuizStore()
            self.assertSetEqual(
                set(expected),
                set(store._get_quiz_files_from_directory("q"))
            )

    def test_get_test_files_ignores_non_json_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.txt']):
            expected = {"q/a.json"}
            store = QuizStore()
            self.assertSetEqual(
                expected,
                set(store._get_quiz_files_from_directory("q"))
            )

    def test_get_summary_handles_empty_lists(self):
        store = QuizStore()
        actual = store._get_quiz_summaries_from_file_list([])
        self.assertEqual([], list(actual))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_one_summary(self):
        store = QuizStore()
        json_for_file = dict(name='pass', title='a test that passes')
        with patch('json.load', return_value=json_for_file):
            expected = {('pass', 'a test that passes', 'd/pass.json')}
            actual = store._get_quiz_summaries_from_file_list(['d/pass.json'])
            self.assertSetEqual(set(expected), set(actual))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_multiple_summary(self):
        store = QuizStore()
        expected = [
            ('cats', 'a tests about felines', 'd/cats.json'),
            ('dogs', 'explore the canine world', 'd/dogs.json')
        ]
        filenames = [path for (_, _, path) in expected]
        json_docs = [dict(name=name, title=title) for (name, title, _) in
                     expected]

        with patch("json.load", side_effect=json_docs):
            actual = store._get_quiz_summaries_from_file_list(filenames)
            self.assertSetEqual(set(expected), set(actual))

    # Test for empty quiz list
    # Test for no questions in file


if __name__ == '__main__':
    unittest.main()
