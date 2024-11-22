import random
import pyautogui

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
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"Retry attempt {attempt + 1}/{times} failed: {e}")
            print("Max retries reached. Raising exception.")
            raise exceptions[0]
        return wrapper
    return decorator


def calculate_click_coordinates(location):
    """
    Calculate random coordinates within a given bounding box.
    """
    x1 = round(location.left + location.width * 0.2)
    y1 = round(location.top + location.height * 0.2)
    x2 = round(location.left + location.width * 0.8)
    y2 = round(location.top + location.height * 0.8)
    return random.randint(x1, x2), random.randint(y1, y2)
