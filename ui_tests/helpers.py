import os
import sys
from socket import gethostbyname, gethostname, socket
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


def launch_quizzology(port) -> Popen[str]:
    """
    launch the quizzology application
    :param port:
    """
    python = "./venv/bin/python" if os.path.isdir('./venv') else "python"
    return Popen([python, "main.py"],
                 env={**os.environ, "QUIZ_PORT": str(port)})


size_desktop = '1920,1200'
size_mobile_iphone_X = '375,812'
size_mobile_galaxy_s5 = '360,640'


def launch_selenium_chrome(headless: bool):
    setup_path_for_dev_test()

    options = Options()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--window-size=%s' % size_mobile_galaxy_s5)
    return webdriver.Chrome(options=options)


def setup_path_for_dev_test():
    project_root = os.environ.get('IDE_PROJECT_ROOTS', '.')
    chrome_driver_path = os.path.join(project_root, 'webdrivers', sys.platform)
    if os.path.isdir(chrome_driver_path):
        path_env_value = os.environ['PATH']
        path_seperator = os.pathsep
        path_list = path_env_value.split(path_seperator)
        if chrome_driver_path not in path_list:
            path_list.append(chrome_driver_path)
            os.environ['PATH'] = path_seperator.join(path_list)



def local_ip() -> str:
    return gethostbyname(gethostname())

def get_likely_port() -> int:
    """
    This isn't guaranteed to work, but it has the system pick an available
    port, then closes the socket and returns the port.
    Because it closes the socket, the system MAY HAVE ALREADY REUSED IT
    """
    junk_socket = socket()
    junk_socket.bind((local_ip(), 0))
    _, chosen_port = junk_socket.getsockname()
    junk_socket.close()
    return chosen_port
