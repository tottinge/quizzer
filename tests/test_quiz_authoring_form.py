import unittest

from bottle import template
from bs4 import BeautifulSoup
from hamcrest import assert_that, contains_string, not_none


class MyTestCase(unittest.TestCase):
    def test_title_is_displayed(self):
        title = 'Edit Quiz'
        html = template('quiz_authoring_form.tpl', {'title': title})
        assert_that(html, contains_string(title))

    def test_form_exists(self):
        title = 'Edit Quiz'
        html = template('quiz_authoring_form.tpl', {'title': title})
        dom = BeautifulSoup(html, "html.parser")
        form = dom.body.find('form',id='quiz_edit')
        assert_that(form, not_none())


if __name__ == '__main__':
    unittest.main()
