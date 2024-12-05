import math

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

""" CUBIC """
def ease_in_cubic(t: float) -> float:
    """Ease-in cubic easing function."""
    return t ** 3

def ease_out_cubic(t: float) -> float:
    """Ease-out cubic easing function."""
    t -= 1
    return t ** 3 + 1
def ease_in_out_cubic(t: float) -> float:
    """Ease-in-out cubic easing function."""
    if t < 0.5:
        return 4 * t ** 3
    t -= 1
    return (2 * t) ** 3 + 1

""" QUARTIC """
def ease_in_quart(t: float) -> float:
    """Ease-in quartic easing function."""
    return t ** 4
def ease_out_quart(t: float) -> float:
    """Ease-out quartic easing function."""
    t -= 1
    return 1 - t ** 4

def ease_in_out_quart(t: float) -> float:
    """Ease-in-out quartic easing function."""
    if t < 0.5:
        return 8 * t ** 4
    t -= 1
    return 1 - 8 * t ** 4

""" QUINTIC  """
def ease_in_quint(t: float) -> float:
    """Ease-in quintic easing function."""
    return t ** 5

def ease_out_quint(t: float) -> float:
    """Ease-out quintic easing function."""
    t -= 1
    return t ** 5 + 1

def ease_in_out_quint(t: float) -> float:
    """Ease-in-out quintic easing function."""
    if t < 0.5:
        return 16 * t ** 5
    t -= 1
    return 1 + 16 * t ** 5


def ease_in_quad(t: float) -> float:
    """Ease-in quadratic easing function."""
    return t * t
