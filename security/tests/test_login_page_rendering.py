import unittest
from typing import Optional

from bottle import template
from bs4 import BeautifulSoup
from hamcrest import assert_that, empty, contains_string, is_not, is_


class MyTestCase(unittest.TestCase):
    def render_the_form(self, page_title='Login', flash='', destination=''):
        html = template('views/login.tpl', {
            "title": page_title,
            "flash": flash,
            "destination": destination
        })
        return BeautifulSoup(html, "html.parser")

    def test_title_appears_in_body(self):
        page_title = 'blah'
        dom: BeautifulSoup = self.render_the_form(page_title=page_title)
        [title_tag_in_body] = dom.body.select("h1", class_="page-title")
        self.assertIn(page_title, str(title_tag_in_body))

    def test_flash_not_displayed_when_absent(self):
        dom: BeautifulSoup = self.render_the_form(flash='')
        flash_sections = dom.body.select("section", id="flash")
        assert_that(flash_sections, empty())

    def test_flash_displayed_if_present(self):
        message = 'OMGFLASH'
        dom: BeautifulSoup = self.render_the_form(flash=message)
        flash_sections = dom.body.select("section", id="flash")
        assert_that(flash_sections, is_not(empty()))
        flash: BeautifulSoup
        [flash] = flash_sections
        assert_that(flash.text, contains_string(message))

    def test_destination_passed_through_hidden_field(self):
        expected_destination = "/go/here/after/login"
        dom: BeautifulSoup = self.render_the_form(
            destination=expected_destination)
        destination: Optional[BeautifulSoup] = dom.body.form.find(
            name="input", attrs={"type": "hidden", "name": "destination"}
        )
        assert_that(destination, is_not(None))
        assert_that(destination['value'], is_(expected_destination))


if __name__ == '__main__':
    unittest.main()
