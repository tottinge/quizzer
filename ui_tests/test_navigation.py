import unittest
from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, equal_to
from selenium.webdriver.chrome.webdriver import WebDriver

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
        cls.browser = launch_selenium_chrome()


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

    def test_select_a_quiz(self):
        browser = self.browser
        browser.get(self.base_url)
        link = browser.find_element_by_link_text('Cats Quiz')
        link.click()
        assert_that(browser.title, equal_to("Cats Quiz"))
        # Here is the fun part. How do we wait for the page to load?
        # WebDriverWait(browser, 2).until(
        #     expected_conditions.presence_of_element_located((title_contains, 'Cats'))
        # )





if __name__ == '__main__':
    unittest.main()
