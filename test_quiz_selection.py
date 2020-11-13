import json
import os
from unittest import TestCase, skip
from unittest.mock import patch, mock_open

from bs4 import BeautifulSoup

from main import render_menu_of_quizzes, get_quiz_summary
from main import QUIZ_STORE



class TestQuizSelection(TestCase):

    @patch("os.listdir", return_value=[])
    def test_title_appears_as_title(self, *_):
        title = "Page Title"
        soup = self.render(title=title, directory='')
        found = soup.head.title.string
        self.assertIn(title, found, f"Did not find '{title}' as page title, found '{found}' instead")

    @patch("os.listdir", return_value =['a.json', 'b.json'])
    @patch("json.load", side_effect = [
        dict(name='a', title="a test"),
        dict(name='b', title='b.test')
    ])
    def test_list_of_quizzes_from_quizzes_directory(self, summary_mock, *_):
        with patch('main._summary_from_file', side_effect = [
            ("a", "a test", "quizzes_dir/a.json"),
            ("b", "b test", "quizzes_dir/b.json")
        ]):
            page = self.render("_", "quizzes_dir")

            menu_items = page.body.find_all('a', class_='quiz_selection')

            actual = [(b['href'], b.text) for b in menu_items]
            expected = {('/quizzes_dir/a.json', 'a test'), ('/quizzes_dir/b.json', 'b test')}
            self.assertSetEqual(expected, set(actual))


    def test_get_a_list_of_test_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.json']):
            expected = "q/a.json", "q/b.json"
            self.assertSetEqual(
                set(expected),
                set(QUIZ_STORE.get_quiz_files("q"))
            )

    def test_get_test_files_ignores_non_json_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.txt']):
            expected = {"q/a.json"}
            self.assertSetEqual(
                expected,
                set(QUIZ_STORE.get_quiz_files("q"))
            )

    def test_get_summary_handles_empty_lists(self):
        self.assertEqual([], get_quiz_summary([]))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_one_summary(self):
        json_for_file = dict(name='pass', title='a test that passes')
        with patch('json.load', return_value =json_for_file):
            expected = {('pass', 'a test that passes', 'd/pass.json')}
            actual = get_quiz_summary(['d/pass.json'])
            self.assertSetEqual(set(expected), set(actual))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_multiple_summary(self):
        expected = [
            ('cats', 'a tests about felines', 'd/cats.json'),
            ('dogs', 'explore the canine world', 'd/dogs.json')
        ]
        filenames = [ path for (_,_,path) in expected]
        json_docs = [ dict(name=name, title=title) for (name,title,_) in expected ]

        with patch("json.load", side_effect = json_docs):
            actual = get_quiz_summary(filenames)
            self.assertSetEqual(set(expected), set(actual))


    def render(self, title, directory):
        markup = render_menu_of_quizzes(title, directory)
        return BeautifulSoup(markup, "html.parser")
