import unittest
from http import HTTPStatus
from urllib.parse import urlparse

from hamcrest import assert_that, is_
from webtest import TestApp, TestResponse

import main

HOME_PAGE = '/study'


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(main.app)

    def test_login_page_loads(self):
        self.app.get("/login")

    def test_post_to_auth_with_no_destination_specified_goes_to_home_page(self):
        response: TestResponse = self.app.post("/auth", {
            'user_name': 'poo',
            'password': 'poopw',
            'destination': ''
        })
        destination_url = response.headers.get('Location')
        destination_path = urlparse(destination_url).path
        assert_that(destination_path, is_(HOME_PAGE))
        assert_that(response.status_code, is_(HTTPStatus.FOUND))


if __name__ == '__main__':
    unittest.main()
