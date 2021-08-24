from unittest import TestCase

from bottle import template
from bs4 import BeautifulSoup

doomed_QUIZ_STORE = None


class TestQuizSelection(TestCase):

    def test_title_appears_as_title(self):
        title = "Page Title"
        soup = self.render(title=title, choices=[])
        found = soup.head.title.string
        self.assertIn(title, found,
                      f"Did not find '{title}' as page title, found '{found}' instead"
                      )

    def test_renders_menu_with_links_to_quizzes(self):
        page = self.render("_", choices=[
            ('a', 'a test', 'unused'),
            ('b', 'b test', 'unused')
        ])
        menu_items = page.body.find_all('a', class_='quiz_selection')
        actual = [(b['href'], b.text.strip()) for b in menu_items]
        expected = {
            ('/study/a', 'a test'),
            ('/study/b', 'b test')}
        self.assertSetEqual(expected, set(actual))

    def render(self, title, choices):
        markup = template("quiz_selection",
                          dict(title=title, choices=choices),
                          template_lookup=['./views','./apps/studying/views'])
        return BeautifulSoup(markup, "html.parser")
