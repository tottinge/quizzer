import unittest
from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, equal_to
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import title_contains
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests.helpers import launch_quizzology, launch_selenium_chrome, \
    get_likely_port


class TestNavigation(TestCase):
    """
    TODO: Configure url/port to use local or docker images
    """
    browser: WebDriver = None
    app: Popen[str] = None
    base_url: str = ""

    @classmethod
    def setUpClass(cls):
        port_number = get_likely_port()
        cls.base_url = f"http://0.0.0.0:{port_number}"
        cls.app = launch_quizzology(port_number)
        cls.browser = launch_selenium_chrome(headless=True)


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

    def test_select_a_quiz(self):
        browser = self.browser
        browser.get(self.base_url)
        link = browser.find_element_by_link_text('Cats Quiz')
        link.click()
        self.wait_for_page_titled("Cats")
        assert_that(browser.title, equal_to("Cats Quiz"))

    def test_answer_a_question(self):
        browser = self.browser
        browser.get(self.base_url + "/quizzes/catsquiz")


    def wait_for_page_titled(self, page_title):
        "Helper method for title-based waits"
        WebDriverWait(self.browser, 2).until(
            expected_conditions.title_contains(page_title)
        )


if __name__ == '__main__':
    unittest.main()
