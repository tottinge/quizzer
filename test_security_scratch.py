import unittest
from unittest import skip

from hamcrest import assert_that, is_, is_not
import bottle


def check(user, pw):
    return True  # ANYTHING GOES!!!!


app = bottle.app()


@bottle.route('/')
@bottle.auth_basic(check)
def home():
    return {'reached': True}


class MyTestCase(unittest.TestCase):

    def test_no_credentials(self):
        x = home()
        if isinstance(x, bottle.HTTPError):
            assert_that(x.status_code, is_(401))  # Access Denied
        pass

    def test_valid_credentials(self):
        from boddle import boddle
        with boddle(params=dict(name='tim', password='Password1!')):
            x = home()
            assert_that(x.status_code, is_not(401))


if __name__ == '__main__':
    unittest.main()
