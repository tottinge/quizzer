import unittest

import bottle
from hamcrest import assert_that, is_, is_not


def check(user, password):
    print(f"User is :{user}, password is:{password}")
    global poo
    poo = user, password
    return user == "Jack"  # ANYTHING GOES!!!!


app = bottle.app()
poo = None


@bottle.route('/')
@bottle.auth_basic(check)
def home():
    global poo  # Terrible, terrible idea
    return {'reached': True, 'poo': poo}


@bottle.route('/wow')
def wow():
    """Just a terrible idea: don't make passwords available"""
    return f"<p>You should never reveal <em>{poo}</em></p>"


if __name__ == '__main__':
    """If you run this, it asks for a login!"""
    bottle.run()


class MyTestCase(unittest.TestCase):
    """Current problem: going straight to 'home()' bypasses the
    various decorators."""

    def test_no_credentials(self):
        x = home()
        if isinstance(x, bottle.HTTPError):
            assert_that(x.status_code, is_(401))  # Access Denied
        pass

    # @skip("This one isn't ripe yet")
    def test_valid_credentials(self):
        from boddle import boddle
        with boddle(params=dict(name='tim', password='Password1!')):
            x = home()
            assert_that(poo, is_(('tim', 'Password1!')))
            assert_that(x.status_code, is_not(401))


if __name__ == '__main__':
    unittest.main()
