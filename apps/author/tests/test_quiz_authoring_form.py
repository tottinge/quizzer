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
        cls.message = 'success message'
        cls.html = template('apps/author/views/quiz_authoring_form.tpl', {
            'quiz': cls.quiz,
            'title': cls.page_title,
            'raw_quiz': asdict(cls.quiz),
            'schema':{},
            'message': cls.message,
        })
        cls.dom = BeautifulSoup(cls.html, "html.parser")

    def test_title_is_displayed(self):
        dom = self.dom
        tab_title = dom.head.title.text
        assert_that(tab_title, contains_string(self.page_title))
        visible_title = dom.body.header.find('h1', id='title')
        assert_that(visible_title.text, contains_string(self.page_title))

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

    def test_successful_save(self):
        message_on_page = self.dom.find('p', id='post-message')
        assert_that(message_on_page.text, is_(self.message))


if __name__ == '__main__':
    unittest.main()
