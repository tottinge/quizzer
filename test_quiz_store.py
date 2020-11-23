import unittest
from unittest.mock import patch

from main import QuizStore


class QuizStoreTest(unittest.TestCase):
    @patch('os.listdir', return_value=['a.json'])
    @patch('builtins.open')
    @patch('json.load', return_value = dict(name="name",title="a title"))
    def test_it_gets_a_summary_of_test(self, *_):
        store = QuizStore()
        expected = {('name', 'a title', 'quizzes/a.json')}
        actual = store.get_quiz_summaries()
        self.assertSetEqual(expected, set(actual))

    @patch('main.QuizStore.get_quiz_summaries', return_value=[
        ('Testquiz',None,'quizzes/a.json')
    ])
    @patch('main.QuizStore._read_quiz_doc_from_file',
           return_value = dict(name='Testquiz'))
    def test_it_retrieves_a_quiz(self, *_):
        store = QuizStore()
        test_quiz = 'Testquiz'
        actual = store.get_quiz(test_quiz)
        self.assertEqual(test_quiz, actual['name'])

    # Test when a file isn't found
    # Test when the file we load isn't good json
    # test when listdir() fails for notfound
    # Test for empty quiz list
    # Test for no questions in file



if __name__ == '__main__':
    unittest.main()
