import unittest
from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, equal_to, string_contains_in_order
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
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
        self.get_page(self.base_url)
        self.click_link('Cats Quiz')
        self.wait_for_page_titled("Cats")
        assert_that(self.browser.title, equal_to("Cats Quiz"))

    def test_answer_a_question(self):
        self.get_page(self.base_url + "/quizzes/catsquiz")
        self.select_value("Gray")
        self.submit_answer()
        self.wait_for_confirmation()
        text = self.browser.find_element_by_id('confirmation').text
        assert_that(
            text,
            string_contains_in_order('Your answer', 'is correct')
        )

    def get_page(self, url):
        self.browser.get(url)

    def click_link(self, link_text):
        link = self.browser.find_element_by_link_text(link_text)
        link.click()

    def wait_for_confirmation(self):
        self.wait_for_element_with_id("confirmation")

    def submit_answer(self):
        self.click_on_element_with_id('submit_answer')

    def click_on_element_with_id(self, element_id: str):
        self.browser.find_element_by_id(element_id).click()

    def select_value(self, input: str):
        self.browser.find_element_by_xpath(f'//input[@value="{input}"]').click()

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=2).until(
            condition.presence_of_element_located(
                (By.ID, element_id))
        )

    def wait_for_page_titled(self, page_title):
        "Helper method for title-based waits"
        WebDriverWait(self.browser, timeout=2, poll_frequency=0.25).until(
            condition.title_contains(page_title)
        )


if __name__ == '__main__':
    unittest.main()