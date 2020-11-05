import unittest

from bs4 import BeautifulSoup

from main import render_menu_of_quizzes


class TestQuizSelection(unittest.TestCase):

    def test_title_appears_as_title(self):
        title = "Page Title"
        soup = self.render(title=title)
        found = soup.head.title.string
        self.assertIn(title, found, f"Did not find '{title}' as page title, found '{found}' instead")

    def render(self, title):
        markup = render_menu_of_quizzes(title)
        return BeautifulSoup(markup, "html.parser")