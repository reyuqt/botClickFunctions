import pyautogui
import time
import random
from typing import Tuple, List, Optional

from webdriver_click_functions.box import Box
from webdriver_click_functions.utils import get_logger
logger = get_logger('screen')
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
                image_path, region=search_region, confidence=current_confidence, grayscale=True
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