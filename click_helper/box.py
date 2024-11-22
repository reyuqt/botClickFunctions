import random
from typing import Tuple, NamedTuple
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("box")

class Box(NamedTuple):
    left: int
    top: int
    width: int
    height: int

    def as_tuple(self) -> Tuple[int, int, int, int]:
        """Return the Box as a standard tuple."""
        return self.left, self.top, self.width, self.height

    def center(self) -> Tuple[int, int]:
        """Calculate the center point of the box."""
        return self.left + self.width // 2, self.top + self.height // 2

    def calculate_click_coordinates(self) -> Tuple[int, int]:
        """
        Calculate random coordinates within the box.
        """
        logger.debug(f"Calculating click coordinates for Box: {self}")
        x1 = round(self.left + self.width * 0.2)
        y1 = round(self.top + self.height * 0.2)
        x2 = round(self.left + self.width * 0.8)
        y2 = round(self.top + self.height * 0.8)
        coords = (random.randint(x1, x2), random.randint(y1, y2))
        logger.debug(f"Calculated coordinates: {coords}")
        return coords
