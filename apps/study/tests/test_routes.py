from unittest import TestCase

from bs4 import Tag
from hamcrest import assert_that, is_, contains_string, not_none
from webtest import TestApp
import main


class TestRoutes(TestCase):

    def setUp(self):
        self.sut = TestApp(main.app)

    def test_session_page_loads(self):
        response = self.sut.get('/session')
        assert_that(response.status_code, is_(200))

    def test_study_page_loads_and_has_title(self):
        response = self.sut.get('/study')
        assert_that(response.status_code, is_(200))
        title: Tag = response.html.find('title')
        assert_that(title.text, contains_string('Quizzology') )


