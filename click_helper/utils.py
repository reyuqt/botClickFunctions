import random
from typing import Tuple, Optional, NamedTuple

import pyautogui
import logging

from click_helper.box import Box
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("click_helper")

MOUSE_MOVEMENTS = [
    pyautogui.easeInQuad,
    pyautogui.easeOutQuad,
    pyautogui.easeInOutQuad,
    pyautogui.easeInOutSine,
    pyautogui.easeInQuint,
]


def retry(times: int, exceptions: tuple[type(Exception)] = (Exception,)):
    """
    Retry decorator for functions that might fail.

    Args:
        times (int): Number of retries.
        exceptions (tuple): Exceptions to catch and retry.

    Returns:
        Decorated function with retry logic.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    logger.debug(f"Attempt {attempt + 1} for {func.__name__}")
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
            logger.error(f"Max retries reached for {func.__name__}")
            raise exceptions[0]

        return wrapper

    return decorator


def locate_image(
    image_path: str,
    region: Optional[Box] = None,
    confidence: float = 0.8,
    min_confidence: float = 0.5,
    retries: int = 3
) -> Box:
    """
    Locate an image on the screen using pyautogui with retries and confidence adjustment.

    Args:
        image_path (str): Path to the image to locate.
        region (Optional[Box], optional): A region to search within (Box format: left, top, width, height). Defaults to None.
        confidence (float, optional): Initial confidence level for matching (0.0 to 1.0). Defaults to 0.8.
        min_confidence (float, optional): Minimum allowable confidence level. Defaults to 0.5.
        retries (int, optional): Number of retry attempts. Defaults to 3.

    Returns:
        Box: The location of the image as a Box object.

    Raises:
        pyautogui.ImageNotFoundException: If the image cannot be located after retries.
    """
    current_confidence: float = confidence
    search_region = region.as_tuple() if region else None  # Convert Box to tuple if provided

    for attempt in range(1, retries + 1):
        logger.debug(
            f"Attempt {attempt}/{retries} to locate image '{image_path}' "
            f"with confidence {current_confidence}"
        )

        try:
            location = pyautogui.locateOnScreen(
                image_path, region=search_region, confidence=current_confidence
            )
            if location:
                box = Box(location.left, location.top, location.width, location.height)
                logger.info(
                    f"Image '{image_path}' found at {box} "
                    f"with confidence {current_confidence} on attempt {attempt}"
                )
                return box

            logger.warning(
                f"Image '{image_path}' not found on attempt {attempt} "
                f"with confidence {current_confidence}"
            )

            # Adjust confidence for the next attempt
            current_confidence = max(current_confidence - 0.1, min_confidence)

        except Exception as e:
            logger.exception(f"Error locating image '{image_path}' on attempt {attempt}: {e}")

    # If no location is found after all retries
    logger.error(
        f"Failed to locate image '{image_path}' after {retries} attempts "
        f"with minimum confidence {min_confidence}"
    )
    raise pyautogui.ImageNotFoundException(f"Image '{image_path}' not found")


def click_at_coordinates(x: int, y: int, duration_range: Tuple[int, int] = (1, 3)):
    """
    Click at specified coordinates with human-like movement.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        duration_range (tuple): Range for click duration (optional).
    """
    duration = random.uniform(*duration_range)
    pyautogui.click(x, y, tween=random.choice(MOUSE_MOVEMENTS), duration=duration)
    logger.info(f"Clicked at ({x}, {y}) with duration {duration:.2f}")


def click_image(
    image_path: str,
    region: Optional[Box] = None,
    confidence: float = 0.8,
    min_confidence: float = 0.5,
    retries: int = 3,
    x_reduction: float = 0.2,
    y_reduction: float = 0.2,
    duration_range: Tuple[float, float] = (1, 3)
) -> bool:
    """
    Locate an image on the screen and click within it.
    High level function that combines locate_image and click_at_coordinates

    Args:
        image_path (str): Path to the image to locate.
        region (Optional[Box], optional): A region to search within (Box format). Defaults to None.
        confidence (float, optional): Initial confidence level for matching (0.0 to 1.0). Defaults to 0.8.
        retries (int, optional): Number of retry attempts. Defaults to 3.
        x_reduction (float, optional): Proportion to reduce the width for clicking. Defaults to 0.2.
        y_reduction (float, optional): Proportion to reduce the height for clicking. Defaults to 0.2.
        duration_range (Tuple[float, float], optional): Range for the mouse movement duration. Defaults to (1, 3).

    Returns:
        bool: True if the image was successfully located and clicked, False otherwise.

    Raises:
        pyautogui.ImageNotFoundException: If the image cannot be located after retries.
    """
    try:
        # Step 1: Locate the image on the screen
        box = locate_image(image_path, region=region, confidence=confidence,min_confidence=min_confidence, retries=retries)
        logger.info(f"Located image at: {box}")

        # Step 2: Calculate random click coordinates within the Box
        x, y = box.calculate_click_coordinates(x_reduction=x_reduction, y_reduction=y_reduction)
        logger.info(f"Calculated click coordinates: ({x}, {y})")

        # Step 3: Perform the click
        duration = random.uniform(*duration_range)
        pyautogui.click(x, y, tween=random.choice(MOUSE_MOVEMENTS), duration=duration)
        logger.info(f"Clicked on image at ({x}, {y}) with duration {duration:.2f} seconds")

        return True

    except pyautogui.ImageNotFoundException as e:
        logger.error(f"Image '{image_path}' not found: {e}")
        return False