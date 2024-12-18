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


""" QUAD """


def ease_in_quad(t: float) -> float:
    """Ease-in quadratic easing function."""
    return t * t


def ease_out_quad(t: float) -> float:
    """Ease-out quadratic easing function."""
    return t * (2 - t)


def ease_in_out_quad(t: float) -> float:
    """Ease-in-out quadratic easing function."""
    if t < 0.5:
        return 2 * t * t
    return -1 + (4 - 2 * t) * t


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


def ease_in_back(t: float, overshoot: float = 0.70158) -> float:
    """Ease-in back easing function with customizable overshoot."""
    return t ** 3 - t * overshoot


def ease_out_back(t: float, overshoot: float = 0.70158) -> float:
    """Ease-out back easing function with customizable overshoot."""
    t -= 1
    return t ** 3 + t * overshoot + 1


def ease_in_out_back(t: float, overshoot: float = 0.70158) -> float:
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


""" BOUNCE """


def ease_out_bounce(t: float) -> float:
    """Ease-out bounce easing function."""
    if t < (1 / 2.75):
        return 7.5625 * t * t
    elif t < (2 / 2.75):
        t -= (1.5 / 2.75)
        return 7.5625 * t * t + 0.75
    elif t < (2.5 / 2.75):
        t -= (2.25 / 2.75)
        return 7.5625 * t * t + 0.9375
    else:
        t -= (2.625 / 2.75)
        return 7.5625 * t * t + 0.984375


def ease_in_bounce(t: float) -> float:
    """Ease-in bounce easing function."""
    return 1 - ease_out_bounce(1 - t)


def ease_in_out_bounce(t: float) -> float:
    """Ease-in-out bounce easing function."""
    if t < 0.5:
        return (1 - ease_out_bounce(1 - 2 * t)) / 2
    return (1 + ease_out_bounce(2 * t - 1)) / 2


def custom_easing(t: float) -> float:
    """
    Define your custom easing function here.

    Parameters:
        t: Parameter ranging from 0 to 1.

    Returns:
        Adjusted t based on custom easing logic.
    """
    # Example: Quadratic ease-in followed by linear
    if t < 0.5:
        return 2 * t * t
    return t


EASING_FUNCTIONS = {
    "linear": linear,
    "ease_in_quad": ease_in_quad,
    "ease_out_quad": ease_out_quad,
    "ease_in_out_quad": ease_in_out_quad,
    "ease_in_cubic": ease_in_cubic,
    "ease_out_cubic": ease_out_cubic,
    "ease_in_out_cubic": ease_in_out_cubic,
    "ease_in_quart": ease_in_quart,
    "ease_out_quart": ease_out_quart,
    "ease_in_out_quart": ease_in_out_quart,
    "ease_in_quint": ease_in_quint,
    "ease_out_quint": ease_out_quint,
    "ease_in_out_quint": ease_in_out_quint,
    "ease_in_sine": ease_in_sine,
    "ease_out_sine": ease_out_sine,
    "ease_in_out_sine": ease_in_out_sine,
    "ease_in_expo": ease_in_expo,
    "ease_out_expo": ease_out_expo,
    "ease_in_out_expo": ease_in_out_expo,
    "ease_in_circ": ease_in_circ,
    "ease_out_circ": ease_out_circ,
    "ease_in_out_circ": ease_in_out_circ,
    "ease_in_back": ease_in_back,
    "ease_out_back": ease_out_back,
    "ease_in_out_back": ease_in_out_back,
    "ease_in_elastic": ease_in_elastic,
    "ease_out_elastic": ease_out_elastic,
    "ease_in_out_elastic": ease_in_out_elastic,
    "ease_in_bounce": ease_in_bounce,
    "ease_out_bounce": ease_out_bounce,
    "ease_in_out_bounce": ease_in_out_bounce,
}
