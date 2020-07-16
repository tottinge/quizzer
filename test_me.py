import unittest.mock
from bs4 import BeautifulSoup

from main import render_html, render_question


class TestSomeStuff(unittest.TestCase):

    def test_document_should_be_html(self):
        pass

    def test_title_appears_as_title(self):
        title = "fred"
        soup = self.render(title=title)
        found = soup.head.find('title').text
        self.assertIn(title, found, f"Did not find {title} in [{found}]")

    def test_title_appears_in_page_body(self):
        title = "fred"
        soup = BeautifulSoup(render_html(title), 'html.parser')
        body_text = soup.body.text
        self.assertIn(title, body_text)

    def question_appears_in_selection_body(self):
        question = 'Does this question appear?'
        soup = self.render(question=question)
        selection = soup.body.selection
        self.assertIn(question, selection.text)

    def render(self, title="_", question='?', answers=[]):
        document = {
            'title':title,
            'questions':[
                {
                    'question':question,
                    'answers':answers
                }
            ]
        }
        markup = render_question(document)
        soup = BeautifulSoup(markup, 'html.parser')
        return soup