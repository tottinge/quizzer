import unittest
from urllib.parse import urlparse, parse_qs

from hamcrest import assert_that, is_

from security.authz import build_login_url


class AuthzTests(unittest.TestCase):
    def test_raw_login_url(self):
        result = build_login_url()
        assert_that(result, is_('/login'))

    def test_login_url_with_destination(self):
        result = build_login_url(destination="anywhere")
        assert_that(result, is_('/login?destination=anywhere'))

    def test_login_url_with_flash(self):
        result = build_login_url(flash="a /dangerous/ string")
        assert_that(result, is_('/login?flash=a+%2Fdangerous%2F+string'))

    def test_login_url_with_flash_and_destination(self):
        flash_message = "message"
        destination_uri = '/poo'
        uri = build_login_url(
            destination=destination_uri,
            flash=flash_message
        )
        result = urlparse(uri)
        parameters = parse_qs(result.query)
        assert_that(parameters['flash'], is_([flash_message]))
        assert_that(parameters['destination'], is_([destination_uri]))
        assert_that(result.path, is_('/login'))


if __name__ == '__main__':
    unittest.main()
