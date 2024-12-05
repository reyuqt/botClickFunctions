import math

import pyautogui
import time
import random
from typing import Tuple, List, Optional, Callable

from webdriver_click_functions.box import Box
from webdriver_click_functions.utils import get_logger
from webdriver_click_functions.screen import locate_image

logger = get_logger("mouse")

pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

MOUSE_MOVEMENTS = [
    pyautogui.easeInQuad,
    pyautogui.easeOutQuad,
    pyautogui.easeInOutQuad,
    pyautogui.easeInOutSine,
    pyautogui.easeInQuint,
    pyautogui.easeInElastic,
    pyautogui.easeInBounce,
]


def ease_in_out_sine(t: float) -> float:
    """Ease-in-out sine function."""
    return -(math.cos(math.pi * t) - 1) / 2

def linear(t: float) -> float:
    """Linear easing function."""
    return t

def calculate_variable_delays(duration: float, steps: int, variation: float = 0.1) -> List[float]:
    """
    Calculate delays with slight random variations.

    Parameters:
        duration: Total duration in seconds.
        steps: Number of steps.
        variation: Maximum variation as a fraction of base delay.

    Returns:
        List of delay times for each step.
    """
    base_delay = duration / steps
    delays = []
    total = 0
    for _ in range(steps+1):
        # Variation between -variation to +variation of the base_delay
        var = base_delay * variation
        delay = random.uniform(base_delay - var, base_delay + var)
        delays.append(delay)
        total += delay
    # Adjust delays to match the total duration
    scaling_factor = duration / total
    scaled_delays = [d * scaling_factor for d in delays]
    return scaled_delays

def generate_cubic_bezier_curve(
        p0: Tuple[int, int],
        p1: Tuple[int, int],
        p2: Tuple[int, int],
        p3: Tuple[int, int],
        steps: int,
        easing_func: Callable[[float], float] = linear
) -> List[Tuple[int, int]]:
    """
    Generate points along a cubic Bezier curve with optional easing.

    Parameters:
        p0: Start point (x, y)
        p1: First control point (x, y)
        p2: Second control point (x, y)
        p3: End point (x, y)
        steps: Number of points to generate
        easing_func: Function to adjust t for easing

    Returns:
        List of points along the curve
    """
    if steps <= 0:
        raise ValueError("Number of steps must be a positive integer.")

    logger.debug(f"Generating Bezier curve: start={p0}, control1={p1}, control2={p2}, end={p3}, steps={steps}")
    points = []
    for i in range(steps + 1):
        t = i / steps
        eased_t = easing_func(t)
        x = (
                (1 - eased_t) ** 3 * p0[0]
                + 3 * (1 - eased_t) ** 2 * eased_t * p1[0]
                + 3 * (1 - eased_t) * eased_t ** 2 * p2[0]
                + eased_t ** 3 * p3[0]
        )
        y = (
                (1 - eased_t) ** 3 * p0[1]
                + 3 * (1 - eased_t) ** 2 * eased_t * p1[1]
                + 3 * (1 - eased_t) * eased_t ** 2 * p2[1]
                + eased_t ** 3 * p3[1]
        )
        points.append((int(x), int(y)))
    logger.debug(f"Generated {len(points)} points along the curve.")
    return points


def click_with_bezier(
        target: Tuple[int, int],
        duration: float = 1,
        steps: int = 200,
        easing_func: Callable[[float], float] = linear,
        variation: float = 0.1,
        pause_chance: float = 0.005,  # .5% chance to pause at any step
        pause_duration: float = 0.05  # Pause duration in seconds
):
    """
    Moves the mouse to the target using a Bezier curve and clicks.

    Parameters:
        target: Tuple of (x, y) specifying the target coordinates.
        duration: Total time in seconds to complete the movement.
        steps: Number of steps for the movement (higher = smoother).
        easing_func: Function to adjust t for easing.
        variation: Maximum variation for delays as a fraction of base delay.
        pause_chance: Probability of pausing at any step.
        pause_duration: Duration of the pause in seconds.
    """
    try:
        # Get the current position of the mouse
        start = pyautogui.position()
        logger.info(f"Starting position: x={start.x}, y={start.y}")
        logger.info(f"Target position: x={target[0]}, y={target[1]}")

        # Calculate vertical distance
        vertical_distance = abs(target[1] - start.y)

        # Define minimum offset
        min_offset = 100
        if vertical_distance >= min_offset:
            # Generate control1 within (min_y, max_y - 100)
            control1_y_lower = min(start.y, target[1])
            control1_y_upper = max(start.y, target[1]) - min_offset
            control2_y_lower = min(start.y, target[1]) + min_offset
            control2_y_upper = max(start.y, target[1])
        else:
            # Adjust offset based on actual distance to prevent negative range
            adjusted_offset = vertical_distance / 2
            control1_y_lower = min(start.y, target[1])
            control1_y_upper = max(start.y, target[1]) - adjusted_offset
            control2_y_lower = min(start.y, target[1]) + adjusted_offset
            control2_y_upper = max(start.y, target[1])

        # Generate two control points for the curve
        control1 = (
            random.randint(round(min(start.x, target[0])), round(max(start.x, target[0]))),
            random.randint(round(control1_y_lower), round(control1_y_upper)),
        )
        control2 = (
            random.randint(round(min(start.x, target[0])), round(max(start.x, target[0]))),
            random.randint(round(control2_y_lower), round(control2_y_upper)),
        )
        logger.info(f"Generated control points: control1={control1}, control2={control2}")

        # Generate points along the cubic Bezier curve with easing
        bezier_points = generate_cubic_bezier_curve(start, control1, control2, target, steps, easing_func)

        # Calculate variable delays between steps
        delays = calculate_variable_delays(duration, steps, variation=variation)
        logger.info(f"Moving mouse along Bezier curve with {steps} steps, total duration {duration} seconds.")

        # Move the mouse through the generated points with variable delays and possible pauses
        for idx, point in enumerate(bezier_points):
            pyautogui.moveTo(point[0], point[1], duration=0)
            time.sleep(delays[idx])

            # Introduce a random pause
            if random.random() < pause_chance:
                logger.debug(f"Pausing for {pause_duration} seconds at step {idx}.")
                time.sleep(pause_duration)

        # Click at the target
        pyautogui.click(target[0], target[1])
        logger.info(f"Clicked at target position: x={target[0]}, y={target[1]}")

    except Exception as e:
        logger.error(f"An error occurred during the Bezier mouse movement: {e}", exc_info=True)


def click_at_coordinates(target: Tuple[int, int], duration: float = 1):
    """
    Click at specified coordinates with human-like movement.

    Args:
        target: Tuple of (x, y) specifying the target coordinates.
        duration_range (tuple): Range for click duration (optional).
        steps_range (tuple): Range for steps amount (optional).
    """
    x, y = target
    pyautogui.click(x, y, logScreenshot=False,
                    tween=random.choice(MOUSE_MOVEMENTS),
                    duration=duration)
    logger.info(f"Clicked at ({x}, {y}) with duration {duration:.2f}")


def click_image(
        image_path: str,
        region: Optional[Box] = None,
        confidence: float = 0.8,
        min_confidence: float = 0.5,
        retries: int = 3,
        x_reduction: float = 0.2,
        y_reduction: float = 0.2,
        duration_range: Tuple[float, float] = (1, 3),
        steps_range: Tuple[int, int] = (150, 300),
        bezier: bool = True,
        easing_func: Callable[[float], float] = linear
) -> bool:
    """
    Locate an image on the screen and click within it.
    """
    try:
        # Step 1: Locate the image on the screen
        box = locate_image(image_path, region=region, confidence=confidence, min_confidence=min_confidence,
                           retries=retries)
        logger.info(f"Located image at: {box}")

        # Step 2: Calculate random click coordinates within the Box
        x, y = box.calculate_click_coordinates(x_reduction=x_reduction, y_reduction=y_reduction)
        logger.info(f"Calculated click coordinates: ({x}, {y})")

        # Step 3: Perform the click
        duration = random.uniform(*duration_range)
        steps = int(random.uniform(*steps_range))
        if bezier:
            click_with_bezier((x, y), duration=duration, steps=steps, easing_func=easing_func)
        else:
            click_at_coordinates(x, duration=duration)
        logger.info(f"Clicked on image at ({x}, {y}) with duration {duration:.2f} seconds")

        return True

    except pyautogui.ImageNotFoundException as e:
        logger.error(f"Image '{image_path}' not found: {e}")
        return False
