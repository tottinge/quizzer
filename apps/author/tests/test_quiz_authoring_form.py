import unittest

import bs4.element
from bottle import template
from bs4 import BeautifulSoup
from hamcrest import assert_that, contains_string, not_none, is_

from quizzes.quiz import Quiz


class StaticFormVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.quiz = Quiz(name="test_quiz", title="This is a test quiz")
        cls.page_title = 'Edit Quiz'
        cls.html = template('apps/author/views/quiz_authoring_form.tpl', {
            'title': cls.page_title,
            'quiz': cls.quiz
        })
        cls.dom = BeautifulSoup(cls.html, "html.parser")

    def test_title_is_displayed(self):
        dom = self.dom
        tab_title = dom.head.title.text
        assert_that(tab_title, contains_string(self.page_title))
        visible_title = dom.body.header.find('h1', id='title')
        assert_that(visible_title.text, contains_string(self.page_title))

    def test_form_exists(self):
        form = self.dom.body.find('form', id='quiz_edit')
        assert_that(form, not_none())

    def test_form_has_fields(self):
        name_input = self.dom.form.find('input', id='quiz_name')
        assert_that(name_input, not_none())
        assert_that(name_input['value'], is_(self.quiz.name))

        title_input = self.dom.form.find('input', id='quiz_title')
        assert_that(title_input, not_none())
        assert_that(title_input['value'], is_(self.quiz.title))

    def test_form_has_submit_button(self):
        button:bs4.element.Tag = self.dom.form.find('button', type='submit', id='save_changes')
        assert_that(button, not_none())
        assert_that(button.text, is_("Save"))

if __name__ == '__main__':
    unittest.main()