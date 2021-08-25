from unittest import TestCase, main

from bs4 import BeautifulSoup
from hamcrest import assert_that, is_, contains_string
from webtest import TestApp, TestResponse

from main import app


class QuickerUITests(TestCase):

    def test_firstTry(self):
        x = TestApp(app)
        response: TestResponse = x.get('/study')
        assert_that(response.status_code, is_(200))
        dom = BeautifulSoup(response.body, 'html.parser')
        assert_that(dom.head.title.text, contains_string("Quizzology"))


if __name__ == '__main__':
    main()
