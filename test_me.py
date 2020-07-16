import unittest.mock
from bs4 import BeautifulSoup


def render_html(title):
    return f'<html><body>{title}</body></html>'


class TestSomeStuff(unittest.TestCase):

    def test_title_appears_on_page(self):
        title = "fred"
        html_doc = render_html(title)
        soup = BeautifulSoup(html_doc, 'html.parser')
        self.assertIn(title, soup.body)