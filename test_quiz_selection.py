from unittest import TestCase
from unittest.mock import patch, mock_open

from bs4 import BeautifulSoup

from main import menu_of_quizzes, quizzology, render_menu_of_quizzes
from quiz_store import QuizStore

doomed_QUIZ_STORE=None

class TestQuizSelection(TestCase):

    def test_title_appears_as_title(self, *_):
        title = "Page Title"
        soup = self.render(title=title, choices=[])
        found = soup.head.title.string
        self.assertIn(title, found,
          f"Did not find '{title}' as page title, found '{found}' instead"
        )

    def test_list_of_quizzes_from_quizzes_directory(self, *_):
        page = self.render("_", choices=[
            ('a', 'a test', 'unused'),
            ('b', 'b test', 'unused')
        ])
        menu_items = page.body.find_all('a', class_='quiz_selection')
        actual = [(b['href'], b.text.strip()) for b in menu_items]
        expected = {
            ('/quizzes/a/0', 'a test'),
            ('/quizzes/b/0', 'b test')}
        self.assertSetEqual(expected, set(actual))


    def render(self, title, choices):
        markup = render_menu_of_quizzes(title, choices)
        return BeautifulSoup(markup, "html.parser")
