import unittest.mock

from bs4 import BeautifulSoup

from main import render_question
from quiz import Quiz


class TestQuizRendering(unittest.TestCase):

    def test_title_appears_in_page_body(self):
        title = "Page Title"
        soup = self.render(title=title)
        [title_tag_in_body] = soup.body.select("h1", class_="page-title")
        self.assertIn(title, str(title_tag_in_body))

    def test_question_appears_in_form(self):
        question = "is this in a form?"
        soup = self.render(question=question)
        selection = soup.body.form
        self.assertIn(question, selection.text)

    def test_answers_appear_in_inputs(self):
        form_body = self.render(decoys=["no"], answer="yes")
        inputs = [tag["value"] for tag in form_body.find_all("input")]
        self.assertIn('yes', inputs)

    def test_page_can_render_with_no_resources(self):
        document = Quiz({
            "title": "no resources at all",
            "name": "resourceless_test",
            "questions": [
                {
                    "question": "Why no resources?",
                    "decoys": ["Who knows?"],
                    "answer": "I'm lazy",
                }
            ]
        })
        page = BeautifulSoup(render_question(document), 'html.parser')
        self.assertIsNone(page.find("section", id="resources"))

    def test_resource_link_appear_in_resource_section(self):
        resource = "Google That", "http://www.google.com"
        page = self.render(resources=[resource])
        actuals = self.getResourceAnchorsFromPage(page)
        self.assertSetEqual(set([resource]), actuals)

    def test_resource_multiple_links(self):
        resources = [
            ("Google That", "http://www.google.com"),
            ("Let Me", "https://lmgtfy.app/?q=calligraphy")
        ]
        page = self.render(resources=resources)
        actual = self.getResourceAnchorsFromPage(page)
        self.assertSetEqual(set(resources), actual)

    def getResourceAnchorsFromPage(self, page):
        resources = page.find('section', id='resources')
        return set(
            (tag.text.strip(), tag['href'])
            for tag in resources.find_all('a')
        )

    def render(self, title="_", name="quiz_name", question="?",
               decoys=["True", "False"], answer="True",
               resources=None):
        document = Quiz({
            "title": title,
            "name": name,
            "questions": [
                {
                    "question": question,
                    "decoys": decoys,
                    "answer": answer,
                    "resources": resources or []
                }
            ]
        })
        markup = render_question(document)
        return BeautifulSoup(markup, "html.parser")
