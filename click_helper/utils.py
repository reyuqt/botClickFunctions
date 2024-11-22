import random
import pyautogui
import logging

# Configure logging
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
    General-purpose retry decorator to handle retries for functions.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    logger.debug(f"Attempt {attempt + 1} for {func.__name__}")
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
            logger.error(f"Max retries reached for {func.__name__}. Raising exception.")
            raise exceptions[0]
        return wrapper
    return decorator


def calculate_click_coordinates(location):
    """
    Calculate random coordinates within a given bounding box.
    """
    logger.debug(f"Calculating click coordinates for location: {location}")
    x1 = round(location.left + location.width * 0.2)
    y1 = round(location.top + location.height * 0.2)
    x2 = round(location.left + location.width * 0.8)
    y2 = round(location.top + location.height * 0.8)
    coords = (random.randint(x1, x2), random.randint(y1, y2))
    logger.debug(f"Calculated coordinates: {coords}")
    return coords