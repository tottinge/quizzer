import json
import unittest
from dataclasses import asdict

import bs4.element
from bottle import template
from bs4 import BeautifulSoup
from hamcrest import assert_that, contains_string, not_none, is_

from quizzes.quiz import Quiz

sample_quiz_json = """
{
    "name":"form-authoring-test",
    "title":"test_quiz_authoring_form basic input",
    "questions":[
        {
            "question": "first sample question",
            "answer": "sample-answer",
            "confirmation":"confirmation for first question",
            "decoys": [
                "q1-decoy1",
                "q1-decoy2"
            ],
            "resources": [
               {"catalog":"https://lmgtfy.app/?q=catalog"},
               {"catamaran":"https://lmgtfy.app/?q=catamaran"}
            ]
        }
    ]
}
"""

class StaticFormVerification(unittest.TestCase):
    quiz: Quiz
    page_title: str
    html: str

    @classmethod
    def setUpClass(cls):
        document = json.loads(sample_quiz_json)
        cls.quiz = Quiz.from_json(document)
        cls.page_title = 'Edit Quiz'
        cls.html = template('apps/author/views/quiz_authoring_form.tpl', {
            'title': cls.page_title,
            'quiz': cls.quiz,
            'raw_quiz': asdict(cls.quiz)
        })
        cls.dom = BeautifulSoup(cls.html, "html.parser")

    def test_title_is_displayed(self):
        dom = self.dom
        tab_title = dom.head.title.text
        assert_that(tab_title, contains_string(self.page_title))
        visible_title = dom.body.header.find('h1', id='title')
        assert_that(visible_title.text, contains_string(self.page_title))

    def test_form_has_fields(self):
        self.assert_tag_value_matches('quiz_name', self.quiz.name)
        self.assert_tag_value_matches('quiz_title', self.quiz.title)

    def test_first_question_is_displayed(self):
        question = self.quiz.first_question().question
        question_section: BeautifulSoup = self.dom.body.find('section', id='questions')
        assert_that(question_section, is_(not_none()))
        form = question_section.find("details", id="0")
        assert_that(form.summary.text, contains_string(question))
        assert_that(form.find("input", id="q0-text"), is_(not_none()))


    def assert_tag_value_matches(self, tag_name, actual):
        name_input = self.dom.form.find('input', id=tag_name)
        assert_that(name_input, not_none())
        assert_that(name_input['value'], is_(actual))

    def test_form_has_submit_button(self):
        button: bs4.element.Tag = self.dom.form.find(
            'button', type='submit', id='save_changes'
        )
        assert_that(button, not_none())
        assert_that(button.text, is_("Save"))


if __name__ == '__main__':
    unittest.main()
