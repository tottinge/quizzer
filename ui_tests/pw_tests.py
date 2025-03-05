import tempfile
from subprocess import Popen
from unittest import TestCase
from playwright.sync_api import sync_playwright

# If you run  these tests, you MUST run
#      playwright install
# after updating your env via pip -r devtools.txt


from ui_tests.helpers import (
    launch_quizzology,
    get_likely_port,
    local_ip,
)


def login(page, url):
    page.goto(url)
    page.locator("#user_name").fill("perry")
    page.locator("#password").fill("passme")
    page.locator("#login").click()


class BaseUrlTest(TestCase):
    browser = None
    context = None
    page = None
    app: Popen[str]
    base_url: str = ""

    @classmethod
    def setUpClass(cls):
        # Launch the application
        cls.tempDir = tempfile.TemporaryDirectory()
        port_number = get_likely_port()
        host = local_ip()
        cls.base_url = f"http://{host}:{port_number}/"
        cls.app = launch_quizzology(port=port_number, user_path=cls.tempDir.name)

        # Launch Playwright and open a browser
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()

        # Use the `login` helper (adapt it to use Playwright if needed)
        login(cls.page, cls.base_url + "/login")

    @classmethod
    def tearDownClass(cls):
        # Close the Playwright session and terminate the app
        cls.page.close()
        cls.context.close()
        cls.browser.close()
        cls.playwright.stop()
        cls.app.terminate()
        cls.tempDir.cleanup()

    def setUp(self):
        self.page.goto(self.base_url)

    def test_title_exists(self):
        assert self.page.title().lower() == "quizzology"

    def test_return_link_exists(self):
        link = self.page.locator("#return_link")
        href_value = link.get_attribute("href")
        assert href_value == "/"

    def test_quiz_links_by_full_or_partial_text(self):
        assert self.page.locator("text=Cats Quiz").is_visible()
        assert self.page.locator("text=Basics of HTML").is_visible()
        assert self.page.locator(
            "text=evelopment Prac"
        ).is_visible()  # Partial link text
        assert self.page.locator("text=Practic").is_visible()  # Partial link text
        assert self.page.locator(".quiz_selection", has_text="Practice").is_visible()
