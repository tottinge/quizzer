import os
from unittest import TestCase, skip

from hamcrest import *
from selenium import webdriver


@skip("This isn't to be run on the CI/CD pipeline")
class BaseUrlTest(TestCase):
    """
    TODO: Configure url/port to use local or docker images
    """
    base_url = "https://sample-fun-with-programming.herokuapp.com/"

    @classmethod
    def setUpClass(cls):
        os.environ['PATH'] = os.environ['PATH'] + os.pathsep + './webdrivers'
        cls.browser = webdriver.Chrome()

    def setUp(self):
        self.browser.get(self.base_url)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

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
        cats_quiz_link = browser.find_element_by_link_text('Cats Quiz')
        html_quiz_link = browser.find_element_by_link_text('Basics of HTML')
        dev_quiz_link = browser.find_element_by_partial_link_text('evelopment')
        for link in [cats_quiz_link, html_quiz_link, dev_quiz_link]:
            assert_that(link, is_not(None))
        # link.click() follows the link
