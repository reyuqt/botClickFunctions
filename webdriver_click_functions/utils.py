import logging
import os
import math
from typing import Tuple

def get_logger(name=__name__, log_level=logging.INFO, log_file=None):
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid duplicate handlers if logger is already set up
    if logger.hasHandlers():
        return logger

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Create directory if it doesn't exist
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = get_logger("click_helper")

def retry(times: int, exceptions: tuple[type(Exception)] = (Exception,)):
    """
    Retry decorator for functions that might fail.
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


def calculate_human_duration_range(
    start: Tuple[int, int],
    end: Tuple[int, int],
    min_dur: float,
    max_dur: float
) -> Tuple[float, float]:
    """
    Calculate a recommended range for mouse movement duration based on the distance between start and end points.

    Parameters:
        start: Tuple of (x, y) for the starting coordinates.
        end: Tuple of (x, y) for the target coordinates.
        min_dur: Minimum duration for very short distances.
        max_dur: Maximum duration for very long distances.

    Returns:
        A tuple (min_duration, max_duration) for the recommended range of durations, clamped to [min_dur, max_dur].
    """
    # Calculate the Euclidean distance between start and end
    distance = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

    # Assume a maximum reasonable screen distance (e.g., diagonal of a 1920x1080 screen)
    max_distance = math.sqrt(1920**2 + 1080**2)  # Adjust for your screen size

    # Use normalized fraction to calculate scaled durations
    # Ended up removing this one because I didn't want min_dur and max_dur factored into the result, but maybe that would give it some sameness in the same session?
    # like if I set min_dur and max_dur as global vars for the entire session it would be like this user moves in this range
    # scaled_min_dur = min_dur + (distance / max_distance * (max_dur - min_dur) * 0.9)
    # scaled_max_dur = min_dur + (distance / max_distance * (max_dur - min_dur) * 1.1)

    # Calculate unbounded duration based on scaling (scaling independent of min_dur and max_dur)
    # Used mouse_distance_timer.py to tweak this until it felt good
    scaled_min_dur = (distance / max_distance) * 0.5  # Base lower bound
    scaled_max_dur = (distance / max_distance) * 1.1  # Base upper bound

    # Use a square root for faster scaling
    # scaled_min_dur = min_dur + (math.sqrt(distance) / math.sqrt(max_distance)) * (max_dur - min_dur) * 0.5
    # scaled_max_dur = min_dur + (math.sqrt(distance) / math.sqrt(max_distance)) * (max_dur - min_dur) * 0.9

    # Clamp durations to [min_dur, max_dur]
    scaled_min_dur = min(max(scaled_min_dur, min_dur), max_dur)
    scaled_max_dur = min(max(scaled_max_dur, min_dur), max_dur)

    # Return the clamped values
    return round(scaled_min_dur, 2), round(scaled_max_dur, 2)

