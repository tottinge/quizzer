from unittest import TestCase, main

from bs4 import BeautifulSoup
from hamcrest import assert_that, is_, contains_string
from webtest import TestApp, TestResponse

from apps.study import study
from apps.study.study import study_controller
from main import app
from shared.quizzology import Quizzology


class QuickerUITests(TestCase):

    def test_firstTry(self):
        study.use_this_quizzology(Quizzology())
        x = TestApp(app)
        response: TestResponse = x.get('/study')
        assert_that(response.status_code, is_(200))
        dom = BeautifulSoup(response.body, 'html.parser')
        assert_that(dom.head.title.text, contains_string("Quizzology"))


if __name__ == '__main__':
    main()
