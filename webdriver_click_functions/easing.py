import pyautogui

MOUSE_MOVEMENTS = [
    pyautogui.easeInQuad,
    pyautogui.easeOutQuad,
    pyautogui.easeInOutQuad,
    pyautogui.easeInOutSine,
    pyautogui.easeInQuint,
    pyautogui.easeInElastic,
    pyautogui.easeInBounce,
]


def linear(t: float) -> float:
    """Linear easing function."""
    return t


def ease_in_cubic(t: float) -> float:
    """Ease-in cubic easing function."""
    return t ** 3


def ease_out_cubic(t: float) -> float:
    """Ease-out cubic easing function."""
    t -= 1
    return t ** 3 + 1


def ease_in_out_sine(t: float) -> float:
    """Ease-in-out sine function."""
    return -(math.cos(math.pi * t) - 1) / 2


def ease_in_quad(t: float) -> float:
    """Ease-in quadratic easing function."""
    return t * t
