import unittest
from subprocess import Popen
from unittest import TestCase

from selenium.webdriver.chrome.webdriver import WebDriver

from ui_tests.helpers import launch_quizzology, launch_selenium_chrome, \
    take_screenshot


class TestNavigation(TestCase):
    """
    TODO: Configure url/port to use local or docker images
    """
    browser: WebDriver = None
    app: Popen[str] = None
    base_url = "http://0.0.0.0:4444/"

    @classmethod
    def setUpClass(cls):
        cls.app = launch_quizzology()
        cls.browser = launch_selenium_chrome()

    def setUp(self):
        self.browser.get(self.base_url)
        take_screenshot(self.browser, "home_page.png")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

    def test_select_a_quiz(self):
        links = self.browser.find_element_by_tag_name('a')
        pass

if __name__ == '__main__':
    unittest.main()
