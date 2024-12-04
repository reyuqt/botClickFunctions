import os
import tempfile
import time
from typing import Union, Tuple, Optional

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from webdriver_click_functions.mouse import click_image
from webdriver_click_functions.utils import get_logger

logger = get_logger(__name__)


def outline_element(driver: WebDriver, selector: Union[tuple[str, str], WebElement], border_color: str = 'red',
                    border_width: str = '2px'):
    """ adds a border to an element, I found this super useful when locating elements that were just text (think radio options),
    but this introduces possibly being detected by dom observations ( akamai cloudflare )"""
    if isinstance(selector, tuple):
        logger.debug(f'Resolving selector tuple: {selector}')
        element = driver.find_element(*selector)
    else:
        element = selector
    driver.execute_script(
        f"arguments[0].style.border='{border_width} solid {border_color}';", element
    )


def get_element(driver: WebDriver, selector: Union[tuple[str, str], WebElement]) -> WebElement:
    """
    Helper function to resolve a WebElement or locate it using a selector tuple.
    """
    if isinstance(selector, tuple):
        logger.debug(f'Resolving selector tuple: {selector}')
        return driver.find_element(*selector)
    logger.debug(f'Selector is already a WebElement')
    return selector


def save_element(element: WebElement, name: Optional[str] = None) -> str:
    """
    Save a screenshot of a WebElement.

    Parameters:
    element (WebElement): The web element to capture.
    name (Optional[str]): The name of the file to save the screenshot. If not provided, a temporary file will be used.
    delete_on_close (bool): If True, the temporary file will be deleted on close. Default is True.

    Returns:
    str: The full path of the saved screenshot.

    Raises:
    Exception: If the screenshot could not be saved.
    """
    # If a name is provided, save the screenshot with the specific name
    if name is not None:
        filepath = os.path.join(os.getcwd(), f'{name}.png')
        saved = element.screenshot(filepath)
        time.sleep(0.5)  # Allow rendering to stabilize
        if saved:
            logger.info("Saved element to filepath: %s", filepath)
            return filepath

    # Use a temporary file to save the screenshot if no name is provided
    with tempfile.NamedTemporaryFile(suffix=".png", dir='.', delete=False, delete_on_close=False) as temp_file:
        temp_file_path = temp_file.name
        element.screenshot(temp_file_path)
        time.sleep(0.5)  # Allow rendering to stabilize
        logger.info("Saved element as temporary image: %s", temp_file_path)
        # Check if the screenshot was successfully saved
        if not os.path.exists(temp_file_path) or not os.path.getsize(temp_file_path):
            logger.error("Failed to save element screenshot at %s", temp_file_path)
            raise Exception(f"Failed to save element screenshot: {temp_file_path}")

        return temp_file_path


def click_this_element(
        driver: Optional[WebDriver],
        selector: Union[tuple[str, str], WebElement],
        confidence: float = 0.8,
        retries: int = 3,
        x_reduction: float = 0.2,
        y_reduction: float = 0.2,
        duration_range: Tuple[float, float] = (1, 3),
        steps_range: Tuple[int, int] = (150, 300),
) -> bool:
    """
    Locate an element, save it as a temporary image, and click it using our utility function.
    """
    try:
        element = get_element(driver, selector)
        logger.info(f"Located Selenium element: {selector}")

        file_path = save_element(element, 'element_1')

        success = click_image(
            image_path=file_path,
            confidence=confidence,
            retries=retries,
            x_reduction=x_reduction,
            y_reduction=y_reduction,
            duration_range=duration_range,
            steps_range=steps_range
        )

        os.remove(file_path)
        logger.info(f"Temporary image file '{file_path}' deleted.")

        return success

    except Exception as e:
        logger.exception(f"Error in clicking element '{selector}': {e}")
        return False


def click_inside_this_element(driver: Optional[WebDriver],
                         outer_selector: Union[tuple[str, str], WebElement],
                         inner_selector: Union[tuple[str, str], WebElement], confidence: float = 0.8,
                         retries: int = 3,
                         x_reduction: float = 0.2,
                         y_reduction: float = 0.2,
                         duration_range: Tuple[float, float] = (1, 3), ):
    pass
