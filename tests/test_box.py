# tests/test_box.py

import pytest
from unittest.mock import patch
from webdriver_click_functions.box import Box
import random
# Optional: Disable logging during tests to keep test output clean
import logging

logging.disable(logging.CRITICAL)


def test_calculate_click_coordinates_valid_reduction():
    """
    Test that calculate_click_coordinates returns coordinates within the reduced box
    for valid x_reduction and y_reduction values.
    """
    # Define a sample Box
    box = Box(left=100, top=200, width=300, height=400)

    # Define reduction values
    x_reduction = 0.2
    y_reduction = 0.2

    # Calculate expected reduced boundaries
    x_offset = round(box.width * x_reduction)  # 60
    y_offset = round(box.height * y_reduction)  # 80

    reduced_left = box.left + x_offset  # 160
    reduced_top = box.top + y_offset  # 280
    reduced_right = box.left + box.width - x_offset  # 340
    reduced_bottom = box.top + box.height - y_offset  # 520

    # Invoke the method
    x, y = box.calculate_click_coordinates(x_reduction, y_reduction)

    # Assert that the coordinates are within the reduced box
    assert reduced_left <= x < reduced_right, f"x-coordinate {x} out of bounds ({reduced_left}, {reduced_right})"
    assert reduced_top <= y < reduced_bottom, f"y-coordinate {y} out of bounds ({reduced_top}, {reduced_bottom})"


def test_calculate_click_coordinates_no_reduction():
    """
    Test calculate_click_coordinates with no reduction (0.0), meaning the entire box is available.
    """
    box = Box(left=50, top=50, width=100, height=100)

    x_reduction = 0.0
    y_reduction = 0.0

    # Expected boundaries
    reduced_left = box.left
    reduced_top = box.top
    reduced_right = box.left + box.width
    reduced_bottom = box.top + box.height

    x, y = box.calculate_click_coordinates(x_reduction, y_reduction)

    assert reduced_left <= x < reduced_right, f"x-coordinate {x} out of bounds ({reduced_left}, {reduced_right})"
    assert reduced_top <= y < reduced_bottom, f"y-coordinate {y} out of bounds ({reduced_top}, {reduced_bottom})"
