from hamcrest import assert_that, is_
from webtest import TestApp, TestResponse
from main import app, setup_quizzology
from unittest import TestCase, main


class QuickerUITests(TestCase):

    def test_firstTry(self):
        setup_quizzology()
        x = TestApp(app)
        response: TestResponse = x.get('/')
        assert_that(response.status_code, is_(200))

if __name__ == '__main__':
    main()