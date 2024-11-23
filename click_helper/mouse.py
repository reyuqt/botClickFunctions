import pyautogui
import time
import random
import logging
from typing import Tuple, List

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
