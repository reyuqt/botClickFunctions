import random
from typing import Tuple, NamedTuple
from click_helper.utils import get_logger

logger = get_logger("box")

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

    def calculate_click_coordinates(
            self,
            x_reduction: float = 0.2,
            y_reduction: float = 0.2
    ) -> Tuple[int, int]:
        """
        Calculate random coordinates within a dynamically reduced box.

        Args:
            x_reduction (float): Proportion to reduce the width on both sides (default: 0.2).
            y_reduction (float): Proportion to reduce the height on both sides (default: 0.2).

        Returns:
            Tuple[int, int]: A random (x, y) coordinate within the reduced box.

        Raises:
            ValueError: If x_reduction or y_reduction results in invalid dimensions.
        """
        if not (0 <= x_reduction < 0.5) or not (0 <= y_reduction < 0.5):
            raise ValueError("Reduction values must be between 0 and 0.5.")

        logger.debug(f"Calculating click coordinates for Box: {self} with reductions "
                     f"x_reduction={x_reduction}, y_reduction={y_reduction}")

        # Calculate reduced dimensions
        x_offset = round(self.width * x_reduction)
        y_offset = round(self.height * y_reduction)

        reduced_left = self.left + x_offset
        reduced_top = self.top + y_offset
        reduced_right = self.left + self.width - x_offset
        reduced_bottom = self.top + self.height - y_offset

        # Random coordinates within the reduced area
        x = random.randint(reduced_left, reduced_right - 1)
        y = random.randint(reduced_top, reduced_bottom - 1)

        logger.debug(f"Reduced box: left={reduced_left}, top={reduced_top}, "
                     f"right={reduced_right}, bottom={reduced_bottom}")
        logger.debug(f"Calculated coordinates: ({x}, {y})")
        return x, y
