import pyautogui
import time
import random
import logging
from typing import Tuple, List, Optional

from click_helper.box import Box

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

pyautogui.MINIMUM_DURATION = 0
pyautogui.MINIMUM_SLEEP = 0
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

def generate_cubic_bezier_curve(
        p0: Tuple[int, int],
        p1: Tuple[int, int],
        p2: Tuple[int, int],
        p3: Tuple[int, int],
        steps: int
) -> List[Tuple[int, int]]:
    """
    Generate points along a cubic Bezier curve.

    Parameters:
        p0: Start point (x, y)
        p1: First control point (x, y)
        p2: Second control point (x, y)
        p3: End point (x, y)
        steps: Number of points to generate

    Returns:
        List of points along the curve
    """
    logger.debug(f"Generating Bezier curve: start={p0}, control1={p1}, control2={p2}, end={p3}, steps={steps}")
    points = []
    for t in [i / steps for i in range(steps + 1)]:
        x = (
                (1 - t) ** 3 * p0[0]
                + 3 * (1 - t) ** 2 * t * p1[0]
                + 3 * (1 - t) * t ** 2 * p2[0]
                + t ** 3 * p3[0]
        )
        y = (
                (1 - t) ** 3 * p0[1]
                + 3 * (1 - t) ** 2 * t * p1[1]
                + 3 * (1 - t) * t ** 2 * p2[1]
                + t ** 3 * p3[1]
        )
        points.append((int(x), int(y)))
    logger.debug(f"Generated {len(points)} points along the curve.")
    return points


def click_with_bezier(
        target: Tuple[int, int],
        duration: float = 1,
        steps: int = 100
):
    """
    Moves the mouse to the target using a Bezier curve and clicks.

    Parameters:
        target: Tuple of (x, y) specifying the target coordinates.
        duration: Total time in seconds to complete the movement.
        steps: Number of steps for the movement (higher = smoother).
    """
    try:
        # Get the current position of the mouse
        start = pyautogui.position()
        logger.info(f"Starting position: x={start.x}, y={start.y}")
        logger.info(f"Target position: x={target[0]}, y={target[1]}")

        # Randomly generate two control points for the curve
        control1 = (
            random.randint(min(start.x, target[0]), max(start.x, target[0])),
            random.randint(min(start.y, target[1]), max(start.y, target[1]) - 100),
        )
        control2 = (
            random.randint(min(start.x, target[0]), max(start.x, target[0])),
            random.randint(min(start.y, target[1]) + 100, max(start.y, target[1])),
        )
        logger.info(f"Generated control points: control1={control1}, control2={control2}")

        # Generate points along the cubic Bezier curve
        bezier_points = generate_cubic_bezier_curve(start, control1, control2, target, steps)

        # Calculate delay between steps
        delay = duration / steps
        logger.info(f"Moving mouse along Bezier curve with {steps} steps, total duration {duration} seconds.")

        # Move the mouse through the generated points
        for point in bezier_points:
            pyautogui.moveTo(point[0], point[1], duration=0)
            time.sleep(delay)

        # Click at the target
        pyautogui.click(target[0], target[1])
        logger.info(f"Clicked at target position: x={target[0]}, y={target[1]}")

    except Exception as e:
        logger.error(f"An error occurred during the Bezier mouse movement: {e}", exc_info=True)


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


def click_at_coordinates(x: int, y: int, duration_range: Tuple[int, int] = (1, 3), steps_range: Tuple[int, int] = (150,300)):
    """
    Click at specified coordinates with human-like movement.

    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        duration_range (tuple): Range for click duration (optional).
    """
    duration = random.uniform(*duration_range)
    steps = int(random.uniform(*steps_range))
    click_with_bezier((x, y), duration=duration, steps=steps)
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
 steps_range: Tuple[int, int] = (150,300)
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
        click_with_bezier((x,y),duration=duration, steps=steps)
        logger.info(f"Clicked on image at ({x}, {y}) with duration {duration:.2f} seconds")

        return True

    except pyautogui.ImageNotFoundException as e:
        logger.error(f"Image '{image_path}' not found: {e}")
        return False
