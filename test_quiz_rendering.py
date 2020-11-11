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

    def test_page_can_render_with_no_resources(self):
        document = {
            "title":"no resources at all",
            "questions":[
                {
                    "question":"Why no resources?",
                    "answers":["who knows?"]
                }
            ]
        }
        page = BeautifulSoup(render_quiz(document), 'html.parser')
        self.assertIsNone(page.find("section", id="resources"))

    def test_resource_link_appear_in_resource_section(self):
        resource = "Google That", "http://www.google.com"
        page = self.render(resources=[resource,])
        resources = page.find('section', id='resources')
        actuals = set((tag.text,tag.get('href')) for tag in resources.find_all('a'))
        self.assertSetEqual(set([resource,]), actuals)

    def test_resource_multiple_links(self):
        resources = [
            ("Google That", "http://www.google.com"),
            ("Let Me", "https://lmgtfy.app/?q=calligraphy")
        ]
        page = self.render(resources=resources)
        section = page.find('section', id='resources')
        actual = set(
            (tag.text, tag.get('href'))
            for tag in (section.find_all('a'))
        )
        self.assertSetEqual(set(resources), actual)

    def render(self, title="_", question="?", answers=["True","False"], resources=None):
        document = {
            "title":title,
            "questions":[
                {
                    "question":question,
                    "answers":answers,
                    "resources":resources or []
                }
            ]
        }
        markup = render_quiz(document)
        return BeautifulSoup(markup, "html.parser")
