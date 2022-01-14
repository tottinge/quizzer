import unittest
from webtest import TestApp
import main


class TestLoginPage(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(main.app)

    def test_login_page_loads(self):
        response = self.app.get("/login")



if __name__ == '__main__':
    unittest.main()
