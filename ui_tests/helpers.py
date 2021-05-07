import os
import sys
from subprocess import Popen

from hamcrest import assert_that, equal_to
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def take_screenshot(browser, screenshot_name):
    screenshot_dir = "./logs/screenshots"
    if not os.path.isdir(screenshot_dir):
        os.makedirs(screenshot_dir)
    filename = os.path.join(screenshot_dir, screenshot_name)
    saved = browser.save_screenshot(filename)
    assert_that(saved, equal_to(True))


def launch_quizzology() -> Popen[str]:
    """
    launch the quizzology application
    """
    python = "./venv/bin/python" if os.path.isdir('./venv') else "python"
    return Popen([python, "main.py"], env={ **os.environ, "QUIZ_PORT":"4444" })


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