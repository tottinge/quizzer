import os
import sys
from subprocess import Popen
from unittest import TestCase, skip, skipIf

import pytest
from hamcrest import *
from selenium import webdriver


@skipIf(sys.platform != "darwin", "This isn't to be run on the CI/CD pipeline")
@skipIf("RUN_UI" not in os.environ, "You didn't ask to run the UI tests")
class BaseUrlTest(TestCase):
    """
    TODO: Configure url/port to use local or docker images
    """
    base_url = "http://0.0.0.0:4444/"

    @classmethod
    def setUpClass(cls):
        cls.active_server = Popen(
            ["./venv/bin/python main.py"],
            shell=True,
            env={"QUIZ_PORT":"4444"}
        )
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + './webdrivers'
        cls.browser = webdriver.Chrome()

    def setUp(self):
        self.browser.get(self.base_url)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.active_server.terminate()

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
