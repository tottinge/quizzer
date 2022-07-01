from unittest import TestCase

from bottle import template
from bs4 import BeautifulSoup


class TestQuizSelection(TestCase):

    def test_title_appears_as_title(self):
        title = "Page Title"
        soup = render(title, [])
        found = soup.head.title.string
        self.assertIn(
            title, found,
            f"Did not find '{title}' as page title, found '{found}' instead"
        )

    def test_renders_menu_with_links_to_quizzes(self):
        choices = [
            ('a', 'a test', 'unused', '/favicon.ico'),
            ('b', 'b test', 'unused', '/favicon.ico')
        ]
        page = render("_", choices)
        menu_items = page.body.find_all('a', class_='quiz_selection')
        actual = [(b['href'], b.text.strip()) for b in menu_items]
        expected = {
            ('/study/a', 'a test'),
            ('/study/b', 'b test')}
        self.assertSetEqual(expected, set(actual))


def render(title, choices):
    markup = template(
        "quiz_choice",
        dict(title=title, choices=choices),
        template_lookup=['./views', './apps/study/views'],
        role='guest'
    )
    return BeautifulSoup(markup, "html.parser")
