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

from PygameHelper.types import *
from functools import lru_cache

import math


@lru_cache()
def lerp(start: Number, stop: Number, amount: Number) -> float:
    """
    Calculates a number between two numbers at a specific increment
    :param start: Union[int, float]
    :param stop: Union[int, float]
    :param amount: Union[int, float]
    :return: float
    """
    if amount > 1 or amount < 0:
        if amount > 1:
            raise ValueError(f"amount in lerp function is bigger than 1")
        if amount < 0:
            raise ValueError(f"amount in lerp function is smaller than 0")
    return amount * (stop - start) + start


@lru_cache()
def clamp(value: Number, mini: Number, maxi: Number) -> Number:
    """
    it clamps a value between mini and maxi
    :param value: Union[int, float]
    :param mini: Union[int, float]
    :param maxi: Union[int, float]
    :return: Union[int, float]
    """
    return mini if value < mini else value if value < maxi else maxi


@lru_cache()
def remap(
        n: Number, start1: Number, stop1: Number, start2: Number, stop2: Number, within_bounds: bool=False
) -> float:
    """
    it Re-maps a number from one range to another (nothing to do with regex it is just the name)
    :param n: Union[int, float]
    :param start1: Union[int, float]
    :param stop1: Union[int, float]
    :param start2: Union[int, float]
    :param stop2: Union[int, float]
    :param within_bounds: bool=False
    :return: Union[int, float]
    """
    v = ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2
    if not within_bounds:
        return v
    if start2 < stop2:
        return clamp(v, start2, stop2)
    else:
        return clamp(v, stop2, start2)


@lru_cache()
def get_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    it returns the distance between two points
    :param x1: int
    :param y1: int
    :param x2: int
    :param y2: int
    :return: float
    """
    return math.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2))


__all__ = [
    "lerp",
    "clamp",
    "remap",
    "get_distance"
]
