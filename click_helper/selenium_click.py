import time
import os
import tempfile
from typing import Union, Tuple, Optional

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from click_helper.mouse import click_image
from click_helper.utils import get_logger

logger = get_logger(__name__)


def get_element(driver: WebDriver, selector: Union[tuple[str, str], WebElement]) -> WebElement:
    """
    Helper function to resolve a WebElement or locate it using a selector tuple.
    """
    if isinstance(selector, tuple):
        logger.debug(f'Resolving selector tuple: {selector}')
        return driver.find_element(*selector)
    logger.debug(f'Selector is already a WebElement')
    return selector


def save_element(element: WebElement, name: Optional[str] = None, delete_on_close: bool = True) -> str:
    # Step 2: Save the element as a temporary image file
    if name is not None:
        filepath = f'{os.getcwd()}/{name}.png'
        saved = element.screenshot(filepath)
        time.sleep(0.5)  # Allow rendering to stabilize
        if saved:
            logger.info(f"Saved element to filepath: {filepath}")
            return filepath
    with tempfile.NamedTemporaryFile(suffix=".png", dir='.', delete=delete_on_close,
                                     delete_on_close=delete_on_close) as temp_file:
        temp_file_path = temp_file.name
        element.screenshot(temp_file_path)
        time.sleep(0.5)  # Allow rendering to stabilize
        logger.info(f"Saved element as temporary image: {temp_file_path}")

    if not os.path.exists(temp_file_path) or not os.path.getsize(temp_file_path):
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
        )

        # Step 5: Clean up the temporary file
        os.remove(file_path)
        logger.info(f"Temporary image file '{file_path}' deleted.")

        return success

    except Exception as e:
        logger.exception(f"Error in clicking element '{selector}': {e}")
        return False
