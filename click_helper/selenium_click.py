import time
import os
import tempfile
from typing import Union, Callable, Tuple, Optional

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import logging

from click_helper.utils import click_image

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("click_helper")

MAX_ATTEMPTS = 3


def get_element(driver: WebDriver, selector: Union[tuple[str, str], WebElement]) -> WebElement:
    """
    Helper function to resolve a WebElement or locate it using a selector tuple.
    """
    if isinstance(selector, tuple):
        logger.debug(f'Resolving selector tuple: {selector}')
        return driver.find_element(*selector)
    logger.debug(f'Selector is already a WebElement')
    return selector


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

    Args:
        driver (Optional[WebDriver]): The Selenium WebDriver instance, only required if selector is a tuple
        selector (Union[tuple[str, str], WebElement]): A tuple selector pair or a WebElement.
        confidence (float, optional): Initial confidence level for image matching. Defaults to 0.8.
        retries (int, optional): Number of retry attempts for locating the image. Defaults to 3.
        x_reduction (float, optional): Proportion to reduce the width for clicking. Defaults to 0.2.
        y_reduction (float, optional): Proportion to reduce the height for clicking. Defaults to 0.2.
        duration_range (Tuple[float, float], optional): Range for mouse movement duration. Defaults to (1, 3).

    Returns:
        bool: True if the image was successfully located and clicked, False otherwise.

    Raises:
        Exception: If the element cannot be located or saved as an image.
    """
    try:
        # Step 1: Locate the Selenium element
        element = get_element(driver, selector)
        logger.info(f"Located Selenium element: {selector}")

        # Step 2: Save the element as a temporary image file
        with tempfile.NamedTemporaryFile(suffix=".png",dir='.', delete=False) as temp_file:
            temp_file_path = temp_file.name
            element.screenshot(temp_file_path)
            logger.info(f"Saved element '{selector}' as temporary image: {temp_file_path}")

        # Step 3: Validate the saved image
        if not os.path.exists(temp_file_path) or not os.path.getsize(temp_file_path):
            raise Exception(f"Failed to save element screenshot: {temp_file_path}")

        # Step 4: Click the saved image
        success = click_image(
            image_path=temp_file_path,
            confidence=confidence,
            retries=retries,
            x_reduction=x_reduction,
            y_reduction=y_reduction,
            duration_range=duration_range,
        )

        # Step 5: Clean up the temporary file
        os.remove(temp_file_path)
        logger.info(f"Temporary image file '{temp_file_path}' deleted.")

        return success

    except Exception as e:
        logger.exception(f"Error in clicking element '{selector}': {e}")
        return False
