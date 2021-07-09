import unittest

from bottle import template
from hamcrest import assert_that, contains_string


class MyTestCase(unittest.TestCase):
    def test_something(self):
        title = 'Edit Quiz'
        x = template('quiz_authoring_form.tpl', {'title': title})
        assert_that(x, contains_string(title))



if __name__ == '__main__':
    unittest.main()
