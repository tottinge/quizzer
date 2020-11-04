import unittest.mock
from bs4 import BeautifulSoup

from main import render_quiz


class TestSomeStuff(unittest.TestCase):

    def test_title_appears_as_title(self):
        title = "Page Title"
        soup = self.render(title=title)
        found = soup.head.title.string
        self.assertIn(title, found, f"Did not find '{title}' as page title, found '{found}' instead")

    def test_title_appears_in_page_body(self):
        title = "Page Title"
        soup = self.render(title=title)
        [title_tag_in_body] = soup.body.select("h1", class_="page-title")
        self.assertIn(title, title_tag_in_body)

    def test_question_appears_in_form(self):
        question = "is this in a form?"
        soup = self.render(question=question)
        selection = soup.body.form
        self.assertIn(question, selection.text)

    def render(self, title="_", question="?", answers=["True","False"]):
        document = {
            "title":title,
            "questions":[
                {
                    "question":question,
                    "answers":answers
                }
            ]
        }
        markup = render_quiz(document)
        soup = BeautifulSoup(markup, "html.parser")
        return soup
