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


""" SINUSOIDAL """


def ease_in_sine(t: float) -> float:
    """Ease-in sine easing function."""
    return 1 - math.cos((t * math.pi) / 2)


def ease_out_sine(t: float) -> float:
    """Ease-out sine easing function."""
    return math.sin((t * math.pi) / 2)


def ease_in_out_sine(t: float) -> float:
    """Ease-in-out sine easing function."""
    return -(math.cos(math.pi * t) - 1) / 2


""" EXPONENTIAL """


def ease_in_expo(t: float) -> float:
    """Ease-in exponential easing function."""
    if t == 0:
        return 0
    return 2 ** (10 * (t - 1))


def ease_out_expo(t: float) -> float:
    """Ease-out exponential easing function."""
    if t == 1:
        return 1
    return 1 - 2 ** (-10 * t)


def ease_in_out_expo(t: float) -> float:
    """Ease-in-out exponential easing function."""
    if t == 0:
        return 0
    if t == 1:
        return 1
    if t < 0.5:
        return (2 ** (20 * t - 10)) / 1023
    return (2 - 2 ** (-20 * t + 10)) / 1023


""" CIRCULAR """


def ease_in_circ(t: float) -> float:
    """Ease-in circular easing function."""
    return 1 - math.sqrt(1 - t * t)


def ease_out_circ(t: float) -> float:
    """Ease-out circular easing function."""
    t -= 1
    return math.sqrt(1 - t * t)


def ease_in_out_circ(t: float) -> float:
    """Ease-in-out circular easing function."""
    if t < 0.5:
        return (1 - math.sqrt(1 - (2 * t) ** 2)) / 2
    t = 2 * t - 2
    return (math.sqrt(1 - t * t) + 1) / 2


""" BACK """


def ease_in_back(t: float, overshoot: float = 1.70158) -> float:
    """Ease-in back easing function with customizable overshoot."""
    return t ** 3 - t * overshoot


def ease_out_back(t: float, overshoot: float = 1.70158) -> float:
    """Ease-out back easing function with customizable overshoot."""
    t -= 1
    return t ** 3 + t * overshoot + 1


def ease_in_out_back(t: float, overshoot: float = 1.70158) -> float:
    """Ease-in-out back easing function with customizable overshoot."""
    s = overshoot * 1.525
    if t < 0.5:
        return (2 * t) ** 2 * ((s + 1) * 2 * t - s) / 2
    t = 2 * t - 2
    return (t ** 2 * ((s + 1) * t + s) + 2) / 2


""" ELASTIC """


def ease_in_elastic(t: float) -> float:
    """Ease-in elastic easing function."""
    return math.sin(13 * math.pi / 2 * t) * 2 ** (10 * (t - 1))


def ease_out_elastic(t: float) -> float:
    """Ease-out elastic easing function."""
    return math.sin(-13 * math.pi / 2 * (t + 1)) * 2 ** (-10 * t) + 1


def ease_in_out_elastic(t: float) -> float:
    """Ease-in-out elastic easing function."""
    if t == 0:
        return 0
    if t == 1:
        return 1
    t = t * 2
    if t < 1:
        return 0.5 * math.sin(13 * math.pi / 2 * (t)) * 2 ** (10 * (t - 1))
    t -= 1
    return 0.5 * (math.sin(-13 * math.pi / 2 * (t)) * 2 ** (-10 * t) + 2)


def ease_in_quad(t: float) -> float:
    """Ease-in quadratic easing function."""
    return t * t
