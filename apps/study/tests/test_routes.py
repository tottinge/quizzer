from unittest import TestCase

from hamcrest import assert_that, is_, contains_string
from webtest import TestApp

import main


class TestRoutes(TestCase):

    def setUp(self):
        self.sut = TestApp(main.app)

    def test_unauthenticated_user_visiting_session_page_causes_redirect(self):
        response = self.sut.get('/session')
        assert_that(response.status_code, is_(302))
        assert_that(response.headers.get('Location'),
                    contains_string('/login'))
