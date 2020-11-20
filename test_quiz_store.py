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
        ('Tesquiz',None,'quizzes/a.json')
    ])
    def test_it_retrieves_a_quiz(self, *_):
        store = QuizStore()
        test_quiz = 'Testquiz'
        actual = store.get_quiz(test_quiz)
        self.assertEqual(test_quiz, actual['name'])




if __name__ == '__main__':
    unittest.main()
