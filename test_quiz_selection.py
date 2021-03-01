from unittest import TestCase
from unittest.mock import patch, mock_open

from bs4 import BeautifulSoup

from main import render_menu_of_quizzes, set_quiz_store
from quiz_store import QuizStore

doomed_QUIZ_STORE=None

class TestQuizSelection(TestCase):

    def setUp(self):
        global doomed_QUIZ_STORE
        doomed_QUIZ_STORE = QuizStore()
        set_quiz_store(doomed_QUIZ_STORE)

    @patch("os.listdir", return_value=[])
    def test_title_appears_as_title(self, *_):
        title = "Page Title"
        soup = self.render(title=title)
        found = soup.head.title.string
        self.assertIn(title, found,
          f"Did not find '{title}' as page title, found '{found}' instead"
        )

    @patch("main.doomed_QUIZ_STORE.get_quiz_summaries", return_value=[
        ('a', 'a test', 'filename'),
        ('b', 'b test', 'otherfile')
    ])
    def test_list_of_quizzes_from_quizzes_directory(self, *_):
        page = self.render("_")

        menu_items = page.body.find_all('a', class_='quiz_selection')

        actual = [(b['href'], b.text.strip()) for b in menu_items]
        expected = {
            ('/quizzes/a/0', 'a test'),
            ('/quizzes/b/0', 'b test')}
        self.assertSetEqual(expected, set(actual))

    def test_get_a_list_of_test_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.json']):
            expected = "q/a.json", "q/b.json"
            self.assertSetEqual(
                set(expected),
                set(doomed_QUIZ_STORE._get_quiz_files_from_directory("q"))
            )

    def test_get_test_files_ignores_non_json_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.txt']):
            expected = {"q/a.json"}
            self.assertSetEqual(
                expected,
                set(doomed_QUIZ_STORE._get_quiz_files_from_directory("q"))
            )

    def test_get_summary_handles_empty_lists(self):
        actual = doomed_QUIZ_STORE._get_quiz_summaries_from_file_list([])
        self.assertEqual([], list(actual))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_one_summary(self):
        json_for_file = dict(name='pass', title='a test that passes')
        with patch('json.load', return_value=json_for_file):
            expected = {('pass', 'a test that passes', 'd/pass.json')}
            actual = doomed_QUIZ_STORE._get_quiz_summaries_from_file_list(['d/pass.json'])
            self.assertSetEqual(set(expected), set(actual))

    @patch('builtins.open', mock_open(read_data=None))
    def test_get_summary_returns_multiple_summary(self):
        expected = [
            ('cats', 'a tests about felines', 'd/cats.json'),
            ('dogs', 'explore the canine world', 'd/dogs.json')
        ]
        filenames = [path for (_, _, path) in expected]
        json_docs = [dict(name=name, title=title) for (name, title, _) in expected]

        with patch("json.load", side_effect=json_docs):
            actual = doomed_QUIZ_STORE._get_quiz_summaries_from_file_list(filenames)
            self.assertSetEqual(set(expected), set(actual))

    def render(self, title):
        markup = render_menu_of_quizzes(title)
        return BeautifulSoup(markup, "html.parser")
