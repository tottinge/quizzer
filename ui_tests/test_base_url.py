import os
import sys
from subprocess import Popen
from unittest import TestCase, skipIf

from hamcrest import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@skipIf(sys.platform != "darwin", "This isn't to be run on the CI/CD pipeline")
class BaseUrlTest(TestCase):
    """
    TODO: Configure url/port to use local or docker images
    """
    browser = None
    app = None
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
        # How/whether to set driver path for github?
        options = Options()
        options.add_argument('--headless')
        return webdriver.Chrome(options=options)

    @staticmethod
    def launch_quizzology():
        popen: Popen[str] = Popen(["./venv/bin/python main.py"], shell=True, env={"QUIZ_PORT": "4444"})
        return popen

    def setUp(self):
        self.browser.get(self.base_url)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

    def test_title_exists(self):
        assert_that(self.browser.title, equal_to_ignoring_case('quizzology'))

    def test_return_link_exists(self):
        # Todo: make back-link testable
        # Here is an example of a problem - we didn't give any way to identify the
        # return link under the lightbulb image. We need to fix this to make it
        # testable
        pass

    def test_quiz_links_exist(self):
        browser = self.browser
        browser.find_element_by_link_text('Cats Quiz')
        browser.find_element_by_link_text('Basics of HTML')
        browser.find_element_by_partial_link_text('evelopment')
        # link.click() follows the link
