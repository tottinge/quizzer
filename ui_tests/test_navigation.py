"""
test_navigation.py

A series of UI tests to ensure that basic behaviors of navigating the
quiz app are not broken for quiz-takers.
"""
import logging
import unittest
from subprocess import Popen
from unittest import TestCase

from hamcrest import assert_that, equal_to, contains_string
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.wait import WebDriverWait

from ui_tests.helpers import launch_quizzology, launch_selenium_chrome, \
    get_likely_port, local_ip, login

CATS_QUIZ = "/study/catsquiz"
logging.basicConfig(level=logging.DEBUG)

# TODO: Create a userStoreFile in a temp directory for the quizzology instance
class TestNavigation(TestCase):
    browser: WebDriver
    app: Popen[str]
    base_url: str = ""

    @classmethod
    def setUpClass(cls):
        port_number = get_likely_port()
        host = local_ip()
        cls.base_url = f"http://{host}:{port_number}"
        logging.debug("base_url is {cls.base_url}")
        cls.app = launch_quizzology(port_number)
        cls.browser = launch_selenium_chrome(headless=True)
        login(cls.browser, cls.base_url + "/login")





    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        cls.app.terminate()

    def test_select_a_quiz(self):
        self.get_page("/")
        self.click_link('Cats Quiz')
        self.wait_for_page_titled("Cats")
        assert_that(self.browser.title, equal_to("Cats Quiz"))

    def test_answer_a_question_correctly_and_get_confirmation(self):
        self.reset_session()
        self.get_page(CATS_QUIZ)
        self.select_value("Gray")
        self.submit_answer()
        self.wait_for_confirmation('confirm_correct')
        text = self.browser.find_element(By.ID, 'confirm_correct').text
        assert_that(text, contains_string('is correct'))

    def test_answer_a_question_incorrectly_and_get_badNews(self):
        self.reset_session()
        self.get_page(CATS_QUIZ)
        self.select_value("Fluffybutt")
        self.submit_answer()
        self.wait_for_confirmation("confirm_incorrect")
        text = self.browser.find_element(By.ID, 'confirm_incorrect').text
        assert_that(text, contains_string("not what we're looking for"))

    def test_complete_a_quiz_perfectly(self):
        self.reset_session()
        self.get_page(CATS_QUIZ)
        for answer in ["Gray", "Jack", "Fluffybutt", "Gray", "Phydeaux"]:

            self.select_value(answer)
            self.submit_answer()
            self.wait_for_confirmation('confirm_correct')

            link_text = 'Next Question'
            next_tags = self.browser.find_elements(By.LINK_TEXT, link_text)
            if next_tags:
                next_tags[0].click()
                self.wait_for_page_titled("Cats")  # Don't jump the gun.

        text = self.browser.find_element(By.ID, 'quiz_performance').text
        assert_that(text, contains_string("perfectly"))

    def reset_session(self):
        self.get_page("/")

    # complete imperfectly

    def get_page(self, relative_page):
        self.browser.get(self.base_url + relative_page)

    def click_link(self, link_text):
        link = self.browser.find_element(By.LINK_TEXT, link_text)
        link.click()

    def wait_for_confirmation(self, element_id):
        self.wait_for_element_with_id(element_id)

    def submit_answer(self):
        self.click_on_element_with_id('submit_answer')

    def click_on_element_with_id(self, element_id: str):
        self.browser.find_element(By.ID, element_id).click()

    def select_value(self, value: str):
        selector = f'//input[@value="{value}"]'
        self.browser.find_element(By.XPATH, selector).click()

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=2).until(
            condition.presence_of_element_located(
                (By.ID, element_id))
        )

    def wait_for_page_titled(self, page_title):
        WebDriverWait(self.browser, timeout=2, poll_frequency=0.25).until(
            condition.title_contains(page_title)
        )


if __name__ == '__main__':
    unittest.main()
