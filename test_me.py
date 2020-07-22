import unittest.mock
from bs4 import BeautifulSoup

from main import render_question


class TestSomeStuff(unittest.TestCase):

    def test_title_appears_as_title(self):
        title = "fred"
        soup = self.render(title=title)
        found = soup.head.find('title').text
        self.assertIn(title, found, f"Did not find {title} in [{found}]")

    def test_title_appears_in_page_body(self):
        title = "fred"
        soup = self.render(title)
        body_text = soup.body.text
        self.assertIn(title, body_text)

    def test_question_appears_in_selection_body(self):
        question = 'Does this question appear?'
        soup = self.render(question=question)
        selection = soup.body.selection
        self.assertIn(question, selection.text)

    def test_question_appears_in_form(self):
        question = "is this in a form?"
        soup = self.render(question=question)
        selection = soup.body.form
        self.assertIn(question, selection.text)

    def render(self, title="_", question='?', answers=['True','False']):
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