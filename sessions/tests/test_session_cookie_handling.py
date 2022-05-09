import unittest

from bottle import LocalRequest, LocalResponse

from sessions.session_id import (
    drop_client_session_id,
    get_client_session_id,
    SESSION_COOKIE_ID
)


class TestSessionCookieHandling(unittest.TestCase):

    @staticmethod
    def fresh_session_objects():
        return LocalRequest(), LocalResponse()

    @staticmethod
    def cookies_from_response(response):
        """Extract cookies into a dictionary from the response
        without violating encapsulation"""
        entries = [value.split(';')[0] for (key, value) in response.headerlist
                   if key == 'Set-Cookie']
        return dict((value.split('=', 1)) for value in entries)

    def get_session_cookie(self, response):
        cookies = self.cookies_from_response(response)
        session_cookie_id = cookies.get(SESSION_COOKIE_ID)
        return session_cookie_id

    def test_create_session_cookie(self):
        request, response = self.fresh_session_objects()

        session_id = get_client_session_id(request, response)

        self.assertIsNotNone(
            session_id,
            "Cookies should be created when needed"
        )
        self.assertIsNotNone(
            self.get_session_cookie(response),
            "Cookies should be set in the response object"
        )

    def test_retains_session_cookie(self):
        request, response = self.fresh_session_objects()
        request.cookies[SESSION_COOKIE_ID] = "ImFake"

        session_id = get_client_session_id(request, response)

        self.assertEqual("ImFake", session_id)

    def test_can_drop_session_cookie(self):
        """
        Surprisingly, deleting a cookie doesn't remove the Set-Cookie
        header for a value. It merely changes it to a string of double-quotes.
        The header is *asking* the browser to set the cookie to "".
        The real activity takes place on the browser.
        """
        request, response = self.fresh_session_objects()
        old_id = get_client_session_id(request, response)
        drop_client_session_id(response)
        self.assertNotEqual(old_id, self.get_session_cookie(response))
