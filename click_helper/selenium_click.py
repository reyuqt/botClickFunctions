import time
from typing import Union, Callable

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from .utils import retry, calculate_click_coordinates, logger, MOUSE_MOVEMENTS
import pyautogui

MAX_ATTEMPTS = 3

def get_element(driver: WebDriver, selector: Union[tuple[str, str], WebElement], name: str) -> WebElement:
    """
    Helper function to resolve a WebElement or locate it using a selector tuple.
    """
    if isinstance(selector, tuple):
        logger.debug(f'[{name}] Resolving selector tuple: {selector}')
        return driver.find_element(*selector)
    logger.debug(f'[{name}] Selector is already a WebElement')
    return selector



# SCENARIO 1
# I have an element on this webpage that I want to click
