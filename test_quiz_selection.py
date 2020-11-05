import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from main import render_menu_of_quizzes, get_test_files, get_test_summary


class TestQuizSelection(unittest.TestCase):

    def test_title_appears_as_title(self):
        title = "Page Title"
        soup = self.render(title=title)
        found = soup.head.title.string
        self.assertIn(title, found, f"Did not find '{title}' as page title, found '{found}' instead")

    @unittest.skip("Not Implemented Yet")
    def test_list_of_quizzes_from_quizzes_directory(self):
        title = "_"
        directory = "quiz_selection_test"
        expected = [
            ("a", "a test", "quizzes/a.json"),
            ("b", "b test", "quizzes/b.json")
        ]
        page = self.render(title, directory)
        buttons = page.body.find_all('button', class_ = 'quiz_button')
        actual = [ (b.value, b.text) for b in buttons ]
        self.assertSetEqual(set(expected), set(actual))

    def test_get_a_list_of_test_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.json']):
            expected = "q/a.json", "q/b.json"
            self.assertSetEqual(
                set(expected),
                set(get_test_files("q"))
            )

    def test_get_test_files_ignores_non_json_files(self):
        with patch("os.listdir", return_value=['a.json', 'b.txt']):
            expected = { "q/a.json" }
            self.assertSetEqual(
                expected,
                set(get_test_files("q"))
            )
    def test_get_names_and_titles_returns_emptylists(self):
        self.assertEqual([], get_test_summary([]))

    def test_get_names_and_titles_returns_summary(self):
        expected = {('pass', 'a tests that passes', 'd/pass.json')}
        actual = get_test_summary(['d/pass.json'])
        self.assertSetEqual(set(expected), set(actual))


    def render(self, title):
        markup = render_menu_of_quizzes(title)
        return BeautifulSoup(markup, "html.parser")