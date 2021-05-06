import os
import sys
from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, equal_to_ignoring_case, equal_to
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class BaseUrlTest(TestCase):
    """
    TODO: Configure url/port to use local or docker images
    """
    browser: WebDriver = None
    app: Popen[str] = None
    base_url = "http://0.0.0.0:4444/"

    @classmethod
    def setUpClass(cls):
        cls.app = cls.launch_quizzology()
        cls.browser = cls.launch_selenium_chrome()

    @staticmethod
    def launch_selenium_chrome():
        if sys.platform == 'darwin':
            os.environ['PATH'] = (
                    os.environ['PATH'] + os.pathsep + './webdrivers'
            )
        options = Options()
        options.add_argument('--headless')
        size_desktop = '1920,1200'
        size_mobile_galaxy_s5 = '360,640'
        size_mobile_iphone_X = '375,812'
        options.add_argument('--window-size=%s' % size_mobile_galaxy_s5)
        return webdriver.Chrome(options=options)

    @staticmethod
    def launch_quizzology() -> Popen[str]:
        """
        launch the quizzology application
        """
        python = "./venv/bin/python" if os.path.isdir('./venv') else "python"
        return Popen([python, "main.py"], env={ **os.environ, "QUIZ_PORT":"4444" })

    def setUp(self):
        self.browser.get(self.base_url)
        self.take_screenshot("home_page.png")

    def take_screenshot(self, screenshot_name):
        screenshot_dir = "./logs/screenshots"
        if not os.path.isdir(screenshot_dir):
            os.makedirs(screenshot_dir)
        filename = os.path.join(screenshot_dir, screenshot_name)
        saved = self.browser.save_screenshot(filename)
        assert_that(saved, equal_to(True))

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

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
        # link.click() follows the link
