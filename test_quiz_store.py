import unittest
from unittest.mock import patch

from main import QuizStore, logger


class QuizStoreTest(unittest.TestCase):
    @patch('os.listdir', return_value=['a.json'])
    @patch('builtins.open')
    @patch('json.load', return_value=dict(name="name", title="a title"))
    def test_it_gets_a_summary_of_test(self, *_):
        store = QuizStore()
        expected = {('name', 'a title', 'quizzes/a.json')}
        actual = store.get_quiz_summaries()
        self.assertSetEqual(expected, set(actual))

    @patch('main.QuizStore.get_quiz_summaries', return_value=[
        ('Testquiz', None, 'quizzes/a.json')
    ])
    @patch('main.QuizStore._read_quiz_doc_from_file',
           return_value=dict(name='Testquiz'))
    def test_it_retrieves_a_quiz(self, *_):
        store = QuizStore()
        test_quiz = 'Testquiz'
        actual = store.get_quiz(test_quiz)
        self.assertEqual(test_quiz, actual['name'])

    # Test when the quiz dir doesn't exist
    @patch('os.listdir', side_effect=FileNotFoundError('boo'))
    def test_returns_empty_list_and_log_exception_if_no_quiz_dir(self, _):
        store = QuizStore()
        store.quiz_dir = 'nonesuch_directory_exists_here'
        with patch.object(logger, 'error') as mock_call:
            returned_summaries = store.get_quiz_summaries()

            self.assertEqual([], returned_summaries)
            (logged_message,) = mock_call.call_args[0]
            self.assertIn('boo', logged_message)



    # Test when the file we load isn't good json



    # test when listdir() fails for notfound
    # Test for empty quiz list
    # Test for no questions in file


if __name__ == '__main__':
    unittest.main()
