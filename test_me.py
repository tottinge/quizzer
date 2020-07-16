import unittest.mock
from bs4 import BeautifulSoup

from main import render_html


class TestSomeStuff(unittest.TestCase):

    def test_document_should_be_html(self):
        pass

    def test_title_appears_in_page_body(self):
        title = "fred"
        html_doc = render_html(title)
        soup = BeautifulSoup(html_doc, 'html.parser')
        found = soup.head.find('title').text
        self.assertIn(title, found, f"Did not find {title} in [{found}]")
