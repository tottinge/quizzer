from unittest import TestCase, main

from bs4 import BeautifulSoup
from hamcrest import assert_that, is_, contains_string
from webtest import TestApp, TestResponse

from main import app, setup_quizzology


class QuickerUITests(TestCase):

    def test_firstTry(self):
        setup_quizzology()
        x = TestApp(app)
        response: TestResponse = x.get('/')
        assert_that(response.status_code, is_(200))
        x = response.body
        dom = BeautifulSoup(response.body, 'html.parser')
        assert_that(dom.head.title.text, contains_string("Quizzology"))


if __name__ == '__main__':
    main()
