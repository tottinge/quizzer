import unittest.mock

from bottle import template
from bs4 import BeautifulSoup

from apps.study.study import LOOKUP_PATH
from apps.study.studycontroller import StudyController
from quizzes.question import Question
from quizzes.quiz import Quiz


class TestQuizRendering(unittest.TestCase):

    def test_title_appears_in_page_body(self):
        title = "Page Title"
        soup = self.render(title=title)
        [title_tag_in_body] = soup.body.select("h1", class_="page-title")
        self.assertIn(title, str(title_tag_in_body))

    def test_question_appears_in_form(self):
        question = "is this in a form?"
        soup = self.render(text=question)
        selection = soup.body.form
        self.assertIn(question, selection.text)

    def test_answers_appear_in_inputs(self):
        form_body = self.render(decoys=["no"], answer="yes")
        inputs = [tag["value"] for tag in form_body.find_all("input")]
        self.assertIn('yes', inputs)

    def test_page_can_render_with_no_resources(self):
        document = Quiz(
            title="no resources at all",
            name="resourceless_test",
            questions=[
                Question(text="Why no resources?", decoys=["Who knows?"],
                         answer="I'm lazy")
            ]
        )
        document = StudyController.prepare_quiz_question_document(document, 0)
        html = template(
            'quiz_question',
            document._asdict(),
            template_lookup=LOOKUP_PATH
        )
        page = BeautifulSoup(html, 'html.parser')
        self.assertIsNone(page.find("section", id="resources"))

    def test_resource_link_appear_in_resource_section(self):
        resource = {
            "text": "Google That",
            "url": "https://www.google.com"
        }
        page = self.render(resources=[resource])
        actual = self.getResourceAnchorsFromPage(page)
        self.assertEqual([resource], actual)

    def test_resource_multiple_links(self):
        resources = [
            {"text": "Google That", "url": "https://www.google.com"},
            {"text": "Let Me", "url": "https://lmgtfy.app/?q=calligraphy"}
        ]
        page = self.render(resources=resources)
        actual = self.getResourceAnchorsFromPage(page)
        self.assertEqual(list(resources), actual)

    @staticmethod
    def getResourceAnchorsFromPage(page):
        resources = page.find('section', id='resources')
        return list(
            {"text": tag.text.strip(), "url": tag['href']}
            for tag in resources.find_all('a')
        )

    @staticmethod
    def render(title="_", name="quiz_name", text="?",
               decoys=("True", "False"), answer="True",
               resources=None):
        document = Quiz(
            title=title,
            name=name,
            questions=[
                Question(text=text, decoys=decoys, answer=answer,
                         resources=resources or [])
            ]
        )
        question_document = StudyController.prepare_quiz_question_document(
            quiz=document, question_number=0
        )
        markup = template(
            'quiz_question',
            question_document._asdict(),
            template_lookup=LOOKUP_PATH
        )
        return BeautifulSoup(markup, "html.parser")
