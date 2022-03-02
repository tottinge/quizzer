from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, equal_to_ignoring_case, equal_to
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from ui_tests.helpers import take_screenshot, launch_quizzology, \
    launch_selenium_chrome, get_likely_port, local_ip


class BaseUrlTest(TestCase):
    browser: WebDriver = None
    app: Popen[str] = None
    base_url: str = ""

    @classmethod
    def setUpClass(cls):
        port_number = get_likely_port()
        host = local_ip()
        cls.base_url = f"http://{host}:{port_number}/"
        cls.app = launch_quizzology(port_number)
        cls.browser = launch_selenium_chrome(headless=True)

    def setUp(self):
        self.browser.get(self.base_url + "study")
        take_screenshot(self.browser, "home_page.png")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

    def test_title_exists(self):
        assert_that(self.browser.title, equal_to_ignoring_case('quizzology'))

    def test_return_link_exists(self):
        link = self.browser.find_element(By.ID, 'return_link')
        href_value = link.get_attribute('href')
        assert_that(href_value, equal_to(self.base_url))

    def test_quiz_links_exist(self):
        browser = self.browser
        browser.find_element(By.LINK_TEXT, "Cats Quiz")
        browser.find_element(By.LINK_TEXT, 'Basics of HTML')
        browser.find_element(By.PARTIAL_LINK_TEXT, 'evelopment')
