# MIT License
#
# Copyright (c) 2021 Emc2356
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
some useful mathematical formulas
"""

import PygameHazel.utils._numba_utils as nbu

import math


@nbu.njit
def lerp(start: float, stop: float, t: float) -> float:
    """
    Calculates a number between two numbers at a specific increment
    :param start: first value
    :param stop: second value
    :param t: the amount of interpolation, it must be between 0 and 1 inclusive
    :type start: float
    :type stop: float
    :type t: float
    :return: float
    """
    return clamp(t, 0, 1) * (stop - start) + start


@nbu.njit
def clamp(value: float, mini: float, maxi: float) -> float:
    """
    it clamps a value between mini and maxi
    :param value: the value that will be clamped
    :param mini: the floor value
    :param maxi: the ceil value
    :type value: float
    :type mini: float
    :type maxi: float
    :return: Union[int, float]
    """
    return mini if value < mini else value if value < maxi else maxi


@nbu.njit
def remap(
        n: float, start1: float, stop1: float, start2: float, stop2: float, within_bounds: bool=False
) -> float:
    """
    it Re-maps a number from one range to another (nothing to do with regex it is just the name)
    :param n: the target value
    :param start1: lower bound of the value's current range
    :param stop1: upper bound of the value's current range
    :param start2: lower bound of the value's target range
    :param stop2: upper bound of the value's target range
    :param within_bounds: constrain the value to the newly mapped range (default=False)
    :type n: float
    :type start1: float
    :type stop1: float
    :type start2: float
    :type stop2: float
    :type within_bounds: bool
    :return: Union[int, float]
    """
    v = ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2
    if not within_bounds:
        return v
    if start2 < stop2:
        return clamp(v, start2, stop2)
    else:
        return clamp(v, stop2, start2)


@nbu.njit
def get_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    it returns the distance between two points
    :param x1: the x position of the first object
    :param y1: the y position of the first object
    :param x2: the x position of the second object
    :param y2: the y position of the second object
    :type x1: float
    :type y1: float
    :type x2: float
    :type y2: float
    :return: float
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


@nbu.njit
def get_distance_squared(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    it returns the distance squared between two points
    :param x1: the x position of the first object
    :param y1: the y position of the first object
    :param x2: the x position of the second object
    :param y2: the y position of the second object
    :type x1: float
    :type y1: float
    :type x2: float
    :type y2: float
    :return: float
    """
    return (x1 - x2) ** 2 + (y1 - y2) ** 2


def build_numba_formulas() -> None:
    lerp(4, 5, 0.5)
    clamp(1, 5, 7)
    clamp(5, 0, 4)
    remap(0.5, -1, 1, -100, 100)
    get_distance(5, 7, 1, 7)
    get_distance_squared(1, 8, 4, 67)


__all__ = [
    "lerp",
    "clamp",
    "remap",
    "get_distance",
    "get_distance_squared"
]
