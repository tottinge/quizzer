import unittest
from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, none
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import title_contains
from selenium.webdriver.support.wait import WebDriverWait

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

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

    def test_select_a_quiz(self):
        browser = self.browser
        link = browser.find_element_by_link_text('Cats Quiz')
        link.click()
        # Here is the fun part. How do we wait for the page to load?
        # WebDriverWait(browser, 2).until(
        #     expected_conditions.presence_of_element_located((title_contains, 'Cats'))
        # )





if __name__ == '__main__':
    unittest.main()
