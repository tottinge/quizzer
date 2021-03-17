from unittest import TestCase
from unittest.mock import patch, mock_open

from bs4 import BeautifulSoup

from main import render_menu_of_quizzes, quizzology
from quiz_store import QuizStore

doomed_QUIZ_STORE=None

class TestQuizSelection(TestCase):

    def setUp(self):
        global doomed_QUIZ_STORE
        doomed_QUIZ_STORE = QuizStore()
        quizzology.set_quiz_store(doomed_QUIZ_STORE)

    @patch("os.listdir", return_value=[])
    def test_title_appears_as_title(self, *_):
        title = "Page Title"
        soup = self.render(title=title)
        found = soup.head.title.string
        self.assertIn(title, found,
          f"Did not find '{title}' as page title, found '{found}' instead"
        )

    @patch("main.quizzology.quiz_store.get_quiz_summaries", return_value=[
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


    def render(self, title):
        markup = render_menu_of_quizzes(title)
        return BeautifulSoup(markup, "html.parser")
