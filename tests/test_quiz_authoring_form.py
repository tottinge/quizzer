import unittest

from bottle import template
from bs4 import BeautifulSoup
from hamcrest import assert_that, contains_string, not_none


class StaticFormVerification(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.title = 'Edit Quiz'
        cls.html = template('quiz_authoring_form.tpl', {'title': cls.title})
        cls.dom = BeautifulSoup(cls.html, "html.parser")

    def test_title_is_displayed(self):
        dom = self.dom
        tab_title = dom.head.title.text
        assert_that(tab_title, contains_string(self.title))
        visible_title = dom.body.header.find('h1', id='title')
        assert_that(visible_title.text, contains_string(self.title))

    def test_form_exists(self):
        form = self.dom.body.find('form',id='quiz_edit')
        assert_that(form, not_none())

    def test_form_has_fields(self):
        name_id = 'quiz_name'
        title_id = 'quiz_title'


if __name__ == '__main__':
    unittest.main()
