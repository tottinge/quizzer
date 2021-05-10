from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, equal_to_ignoring_case, equal_to
from selenium.webdriver.chrome.webdriver import WebDriver

from ui_tests.helpers import take_screenshot, launch_quizzology, \
    launch_selenium_chrome


class BaseUrlTest(TestCase):
    """
    TODO: Configure url/port to use local or docker images
    """
    browser: WebDriver = None
    app: Popen[str] = None
    base_url = "http://0.0.0.0:4444/"

    @classmethod
    def setUpClass(cls):
        cls.app = launch_quizzology(4444)
        cls.browser = launch_selenium_chrome()

    def setUp(self):
        self.browser.get(self.base_url)
        take_screenshot(self.browser, "home_page.png")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()
        cls.app.wait()


    def test_title_exists(self):
        assert_that(self.browser.title, equal_to_ignoring_case('quizzology'))

    def test_return_link_exists(self):
        link = self.browser.find_element_by_id('return_link')
        href_value = link.get_attribute('href')
        assert_that(href_value, equal_to(self.base_url))

    def test_quiz_links_exist(self):
        browser = self.browser
        browser.find_element_by_link_text('Cats Quiz')
        browser.find_element_by_link_text('Basics of HTML')
        browser.find_element_by_partial_link_text('evelopment')


