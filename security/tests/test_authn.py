import unittest
from http import HTTPStatus
from urllib.parse import urlparse

from hamcrest import assert_that, is_, not_none
from webtest import TestApp, TestResponse

import main
from security.authn import make_bearer_token
from shared.user import User

HOME_PAGE = '/'


def redirect_destination_of(response):
    destination_url = response.headers.get('Location')
    destination_path = urlparse(destination_url).path
    return destination_path


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(main.app)

    def test_login_page_loads(self):
        self.app.get("/login")

    def test_guest_auth_with_no_destination_redirects_to_home_page(self):
        response: TestResponse = self.app.post("/auth", {
            'user_name': 'poo',
            'password': 'poopw',
            'destination': ''
        })
        assert_that(redirect_destination_of(response), is_(HOME_PAGE))
        assert_that(response.status_code, is_(HTTPStatus.FOUND))

    def test_guest_auth_with_destination_redirects_to_destination(self):
        desired_page = '/page/I/want'
        response: TestResponse = self.app.post("/auth", {
            'user_name': 'poo',
            'password': 'poopw',
            'destination': desired_page
        })
        assert_that(redirect_destination_of(response), is_(desired_page))
        assert_that(response.status_code, is_(HTTPStatus.FOUND))

    def test_root_sends_unauthenticated_user_to_login_page(self):
        response = self.app.get("/")
        assert_that(redirect_destination_of(response), is_("/login"))
        assert_that(response.status_code, is_(HTTPStatus.FOUND))

    def test_root_sends_expired_user_to_login_page(self):
        user = User(user_name='expired', password='', role='')
        expired_token = make_bearer_token(user, hours_to_live=-1)
        self.app.set_cookie('Authorization', f"Bearer {expired_token}")
        response = self.app.get("/", )
        assert_that(redirect_destination_of(response), is_("/login"))

    def test_root_sends_authenticated_guest_to_homepage(self):
        self.set_auth_for('guest')
        response: TestResponse = self.app.get("/")
        assert_that(response.status_code, is_(HTTPStatus.OK))

    def test_root_sends_authenticated_student_to_homepage(self):
        self.set_auth_for("student")
        response = self.app.get("/")
        assert_that(response.status_code, is_(HTTPStatus.OK))

    def test_root_sends_authenticated_author_to_home_page(self):
        self.set_auth_for("author")
        response: TestResponse = self.app.get("/")
        assert_that(response.status_code, is_(HTTPStatus.OK))
        assert_that(response.html.find('a',id='add_quiz'), not_none())

    def set_auth_for(self, role="student"):
        guest = User(user_name=f"test {role}", password='', role=role)
        guest_token = make_bearer_token(guest)
        self.app.set_cookie('Authorization', f"Bearer {guest_token}")


if __name__ == '__main__':
    unittest.main()
