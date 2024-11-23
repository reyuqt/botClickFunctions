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
pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

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
