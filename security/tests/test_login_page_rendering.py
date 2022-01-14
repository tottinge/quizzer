import unittest

from bottle import template
from bs4 import BeautifulSoup


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    @classmethod
    def setUpClass(cls):
        cls.page_title = 'Edit Quiz'
        cls.html = template('views/login.tpl', {
            "title": "Who are you?",
            "flash": "flash",
            "destination": "destination"
        })

        cls.dom = BeautifulSoup(cls.html, "html.parser")


if __name__ == '__main__':
    unittest.main()

# ToDo - Add assertions for the newly rendered Login page
