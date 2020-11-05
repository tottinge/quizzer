import unittest.mock
from bs4 import BeautifulSoup

from main import render_quiz


class TestQuizRendering(unittest.TestCase):

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

    def test_answers_appear_in_inputs(self):
        answers = ["yes", "no"]
        form_body = self.render(answers=answers)
        inputs = [tag["value"] for tag in form_body.find_all("input")]
        self.assertSetEqual(set(answers), set(inputs))


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
        return BeautifulSoup(markup, "html.parser")
