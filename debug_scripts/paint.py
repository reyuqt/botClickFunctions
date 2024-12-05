from pathlib import Path

import pyautogui
from PIL import Image, ImageDraw
import time
import math
import os
import platform
import subprocess


def move_mouse(path, duration_per_move=0.0000001):
    """
    Moves the mouse along the given path.

    Args:
        path (List[Tuple[int, int]]): List of (x, y) coordinates.
        duration_per_move (float): Duration to move between points.
    """
    for point in path:
        x, y = point
        pyautogui.moveTo(x, y, duration=duration_per_move)
        #time.sleep(duration_per_move)

def visualize_path_on_screenshot(path, save_path='mouse_path.png'):
    """
    Takes a screenshot and draws the mouse path on it.

    Args:
        path (List[Tuple[int, int]]): List of (x, y) coordinates.
        save_path (str): File path to save the visualized image.
    """
    # Take screenshot
    screenshot = pyautogui.screenshot(region=(0,0,1920,1080))
    draw = ImageDraw.Draw(screenshot)

    # Draw the path as a continuous line
    if len(path) > 1:
        draw.line(path, fill='red', width=3)  # Red line with width 3
        # Optionally, draw circles at each point for emphasis
        for point in path:
            draw.ellipse((point[0]-3, point[1]-3, point[0]+3, point[1]+3), fill='blue', outline='blue')

    # Save the image
    screenshot.save(save_path)
    print(f"Path visualized and saved to {save_path}")

def open_image(file_path):
    """
    Opens an image file using the default image viewer based on the OS.

    Args:
        file_path (str): Path to the image file.
    """
    try:
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(['open', file_path])
        elif platform.system() == 'Windows':    # Windows
            os.startfile(file_path)
        else:                                   # Linux variants
            subprocess.call(['xdg-open', file_path])
    except Exception as e:
        print(f"Unable to open image automatically: {e}")


