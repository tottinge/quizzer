import unittest


class TestWithPycharmCorrectly(unittest.TestCase):
    """
    Pycharm is weird and stupid in this regard. If there is no
    test file in the root, it will not offer the option to run
    all tests in project.

    Running from the tests directory doesn't work, because it
    will cd to tests to begin running tests, and we need it to
    run from the root.

    This joy brought to you from IntelliJ
    """

    def test_nothing(self):
        pass


if __name__ == '__main__':
    unittest.main()
