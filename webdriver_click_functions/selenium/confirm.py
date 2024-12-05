import os
import tempfile
import time
from typing import Union, Tuple, Optional, Callable
import re

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC

from webdriver_click_functions.utils import get_logger

logger = get_logger("confirm")

class Clicked:
    """ different methods to verify if an element has been clicked, mostly shortcuts for how I've tested in the past """

    @staticmethod
    def default(driver: WebDriver, element: WebElement) -> bool:
        return driver.switch_to.active_element == element

    @staticmethod
    def selected(driver: WebDriver, element: WebElement) -> bool:
        return element.is_selected()

    @staticmethod
    def navigation(driver: WebDriver, element: WebElement, expected_url) -> bool:
        pass

    @staticmethod
    def injection(driver: WebDriver, element: WebElement) -> bool:
        # we would inject script before click and use event listeners to watch and record changes
        # after click we would check record to see if right thing was clicked
        pass

    @staticmethod
    def has_attribute(driver: WebDriver, element: WebElement, attribute_name: str,
                      attribute_value: Optional[str] = None) -> bool:
        if attribute_value is None:
            return element.get_attribute(attribute_name) is not None
        else:
            return attribute_value in element.get_attribute(attribute_name)

    @staticmethod
    def has_text(element, text: str) -> bool:
        """ use if youre expecting the text to change after click """
        pass

    @staticmethod
    def wait_for_url_regex(driver: WebDriver, url_regex_pattern: str, timeout: int = 10,
                           poll_frequency: float = 0.5) -> bool:
        """
        Waits until the current URL matches the provided regular expression pattern.

        Args:
            driver (WebDriver): Selenium WebDriver instance.
            regex_pattern (str): The regular expression pattern to match against the current URL.
            timeout (int, optional): Maximum time to wait for the URL to match (in seconds). Defaults to 10.
            poll_frequency (float, optional): How often to poll the condition (in seconds). Defaults to 0.5.

        Returns:
            bool: True if the URL matches the regex within the timeout, False otherwise.
        """
        try:
            pattern = re.compile(url_regex_pattern)
            logger.info(f"Waiting for URL to match regex: '{url_regex_pattern}' with timeout={timeout}s")

            # Define the custom expected condition
            def url_matches(driver):
                current_url = driver.current_url
                match = pattern.search(current_url)
                if match:
                    logger.info(f"URL matched regex: '{url_regex_pattern}' | Current URL: '{current_url}'")
                else:
                    logger.debug(f"URL does not match regex: '{url_regex_pattern}' | Current URL: '{current_url}'")
                return match is not None

            # Initialize WebDriverWait with the custom condition
            wait = WebDriverWait(driver, timeout, poll_frequency=poll_frequency)
            wait.until(url_matches)
            return True

        except TimeoutException:
            logger.error(f"Timeout: URL did not match regex '{url_regex_pattern}' within {timeout} seconds.")
            return False
        except re.error as regex_error:
            logger.error(f"Invalid regex pattern '{url_regex_pattern}': {regex_error}")
            return False
        except Exception as e:
            logger.exception(f"An unexpected error occurred while waiting for URL regex match: {e}")
            return False
