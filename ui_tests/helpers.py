import logging
import os
import sys
from socket import gethostbyname, gethostname, socket
from subprocess import Popen

from hamcrest import assert_that, equal_to
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as condition
from selenium.webdriver.support.wait import WebDriverWait


def take_screenshot(browser, screenshot_name):
    screenshot_dir = "./logs/screenshots"
    if not os.path.isdir(screenshot_dir):
        os.makedirs(screenshot_dir)
    filename = os.path.join(screenshot_dir, screenshot_name)
    saved = browser.save_screenshot(filename)
    assert_that(saved, equal_to(True))


def launch_quizzology(port) -> Popen[str]:
    """
    launch the quizzology application
    :param port:
    """
    python = "./venv/bin/python" if os.path.isdir("./venv") else "python"
    subprocess_environ = {
        **os.environ,
        "QUIZ_PORT": str(port),
        "QUIZ_LOG_PATH": "./logs/ui_testing.log",
    }
    return Popen(
        [python, "main.py"],
        env=subprocess_environ,
        text=True,
    )


size_desktop = "1920,1200"
size_mobile_iphone_X = "375,812"
size_mobile_galaxy_s5 = "360,640"


def launch_selenium_chrome(headless: bool) -> WebDriver:
    setup_path_for_dev_test()

    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--window-size=%s" % size_mobile_galaxy_s5)
    return webdriver.Chrome(options=options)


def setup_path_for_dev_test():
    import chromedriver_autoinstaller

    project_root = os.environ.get("IDE_PROJECT_ROOTS", ".")
    chrome_driver_path = os.path.join(project_root, "webdrivers", sys.platform)
    os.makedirs(chrome_driver_path, exist_ok=True)
    path = chromedriver_autoinstaller.install(path=chrome_driver_path)
    os.environ["PATH"] = os.pathsep.join([os.environ["PATH"], path])


def local_ip() -> str:
    hostname = gethostname()
    return os.environ.get("QUIZ_HOST", gethostbyname(hostname))


def get_likely_port() -> int:
    """
    This isn't guaranteed to work, but it has the system pick an available
    port, then closes the socket and returns the port.
    Because it closes the socket, the system MAY HAVE ALREADY REUSED IT
    """
    junk_socket = socket()
    host_name = os.environ.get("QUIZ_HOST", local_ip())
    logging.debug(f"likely_port: Host name is {host_name}")
    junk_socket.bind((host_name, 0))
    _, chosen_port = junk_socket.getsockname()
    junk_socket.close()
    logging.debug(f"likely_port: Chosen port is {chosen_port}")
    return chosen_port


def login(browser: WebDriver, url: str):
    browser.get(url)
    WebDriverWait(browser, timeout=2, poll_frequency=0.25).until(
        condition.title_contains("Who are you")
    )
    browser.find_element(By.NAME, "user_name").send_keys("perry")
    browser.find_element(By.NAME, "password").send_keys("passme")
    browser.find_element(By.ID, "login").click()
