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
perlin noise
"""

import PygameHaze.utils._numba_utils as nbu
from typing import Optional
import numpy as np
import functools
import random
import math

import sys
import os

CORES = os.cpu_count()

_PERLIN_YWRAPB: int = 4
_PERLIN_YWRAP: int = 1 << _PERLIN_YWRAPB
_PERLIN_ZWRAPB: int = 8
_PERLIN_ZWRAP: int = 1 << _PERLIN_ZWRAPB
_PERLIN_SIZE: int = 4095
_octaves: int = 4  # default to medium smooth
_perlin_amp_falloff: float = 0.5  # 50% reduction/octave
_perlin: Optional[np.ndarray] = None  # lazy load it


def _set_seed(cls, seed: int) -> None:
    """
    it sets the seed for the random values of perlin noise
    :param seed: the seed that will be used
    :type seed: int
    :return: None
    """
    global _perlin
    r = random.Random()
    r.seed(seed)
    for i in range(len(_perlin)):
        _perlin[i] = r.random()
    if nbu.USE_NUMBA:
        cls.__call__.recompile()
        cls.noise3D.recompile()
        cls.noise2D.recompile()
        cls.noise1D.recompile()


def _noise_detail(cls, octaves: int = -1, falloff: float = -1) -> None:
    """
    its sets the number of octaves that are going to be used and the falloff factor for each octave
    :param octaves: the numbers of octaves that will be used
    :param falloff: falloff factor for each octave
    :type octaves: int
    :type falloff: float
    :return: None
    """
    global _octaves, _perlin_amp_falloff
    if octaves > 0:
        _octaves = int(octaves)
    if falloff > 0:
        _perlin_amp_falloff = falloff
    if nbu.USE_NUMBA:
        cls.__call__.recompile()
        cls.noise3D.recompile()
        cls.noise2D.recompile()
        cls.noise1D.recompile()


@nbu.njit
def _scaled_cosine(i: float) -> float:
    return 0.5 * (1.0 - math.cos(i * math.pi))


def noise3D(x: float, y: float = 0, z: float = 0) -> float:
    """
    it calculates the 3D perlin noise value based on the random values and the values passed
    :param x: the x value
    :param y: the y value
    :param z: the z value
    :type x: float
    :type y: float
    :type z: float
    :return: float
    """
    xi = int(abs(x))
    yi = int(abs(y))
    zi = int(abs(z))
    xf = abs(x) - xi
    yf = abs(y) - yi
    zf = abs(z) - zi

    value = float(0)
    ampl = float(0.5)

    for _ in range(_octaves):
        of = xi + (yi << _PERLIN_YWRAPB) + (zi << _PERLIN_ZWRAPB)

        rxf = _scaled_cosine(xf)
        ryf = _scaled_cosine(yf)

        n1 = _perlin[of & _PERLIN_SIZE]
        n1 += rxf * (_perlin[(of + 1) & _PERLIN_SIZE] - n1)
        n2 = _perlin[(of + _PERLIN_YWRAP) & _PERLIN_SIZE]
        n2 += rxf * (_perlin[(of + _PERLIN_YWRAP + 1) & _PERLIN_SIZE] - n2)
        n1 += ryf * (n2 - n1)

        of += _PERLIN_ZWRAP
        n2 = _perlin[of & _PERLIN_SIZE]
        n2 += rxf * (_perlin[(of + 1) & _PERLIN_SIZE] - n2)
        n3 = _perlin[(of + _PERLIN_YWRAP) & _PERLIN_SIZE]
        n3 += rxf * (_perlin[(of + _PERLIN_YWRAP + 1) & _PERLIN_SIZE] - n3)
        n2 += ryf * (n3 - n2)

        n1 += _scaled_cosine(zf) * (n2 - n1)

        value += n1 * ampl
        ampl *= _perlin_amp_falloff
        xi <<= 1
        xf *= 2
        yi <<= 1
        yf *= 2
        zi <<= 1
        zf *= 2

        if xf >= 1.0:
            xi += 1
            xf -= 1
        if yf >= 1.0:
            yi += 1
            yf -= 1
        if zf >= 1.0:
            zi += 1
            zf -= 1

    return value


def noise2D(x: float, y: float = 0) -> float:
    """
    it calculates the 2D perlin noise value based on the random values and the values passed
    :param x: the x value
    :param y: the y value
    :type x: float
    :type y: float
    :return: float
    """
    xi = int(abs(x))
    yi = int(abs(y))
    xf = abs(x) - xi
    yf = abs(y) - yi

    value = float(0)
    ampl = float(0.5)

    for _ in range(_octaves):
        of = xi + (yi << _PERLIN_YWRAPB)

        rxf = _scaled_cosine(xf)
        ryf = _scaled_cosine(yf)

        n1 = _perlin[of & _PERLIN_SIZE]
        n1 += rxf * (_perlin[(of + 1) & _PERLIN_SIZE] - n1)
        n2 = _perlin[(of + _PERLIN_YWRAP) & _PERLIN_SIZE]
        n2 += rxf * (_perlin[(of + _PERLIN_YWRAP + 1) & _PERLIN_SIZE] - n2)
        n1 += ryf * (n2 - n1)

        value += n1 * ampl
        ampl *= _perlin_amp_falloff
        xi <<= 1
        xf *= 2
        yi <<= 1
        yf *= 2

        if xf >= 1.0:
            xi += 1
            xf -= 1
        if yf >= 1.0:
            yi += 1
            yf -= 1

    return value


def noise1D(x: float) -> float:
    """
    it calculates the 1D perlin noise value based on the random values and the values passed
    :param x: the x value
    :type x: float
    :return: float
    """
    xi = int(abs(x))
    xf = abs(x) - xi

    value = 0
    ampl = 0.5

    for _ in range(_octaves):
        n1 = _perlin[xi & _PERLIN_SIZE]
        n1 += _scaled_cosine(xf) * (_perlin[(xi + 1) & _PERLIN_SIZE] - n1)

        value += n1 * ampl
        ampl *= _perlin_amp_falloff
        xi <<= 1
        xf *= 2

        if xf >= 1.0:
            xi += 1
            xf -= 1

    return value


# this is a python function as we have to decide in which func to send it as the input array can be 1D or 2D
def fromArray(
    cls, arr: np.ndarray, dim: int = 3, out: Optional[np.ndarray] = None
) -> np.ndarray:
    """
    it calculates the perlin noise values based on the information from arr
    :param arr: the data for perlin noise calculations
    :param dim: the dimensions of the perlin noise calculations
    :param out: a array that the output values will go, if it isn't provided a new array will be created
    :type arr: np.ndarray
    :type dim: int
    :type out: np.ndarray
    :return: np.ndarray
    """
    if dim not in {1, 2, 3}:
        raise ValueError(f"unsupported dimension '{dim}', expected 1, 2 or 3")
    func = getattr(cls, f"noise{dim}D")
    if out is None:
        out = np.ndarray(arr.shape[0])
    if len(arr.shape) == 1:
        cls._fromArr1D(arr, out, func)
    else:
        cls._fromArrayFuncs[dim](arr, out, func)

    return out


def fromArray2D3D(arr: np.ndarray, out: np.ndarray, func) -> None:
    size = arr.shape[0]
    for start in nbu.prange(CORES):
        for i in range(start, size, CORES):
            out[i] = func(arr[i][0], arr[i][1], arr[i][2])


def fromArray2D2D(arr: np.ndarray, out: np.ndarray, func) -> None:
    size = arr.shape[0]
    for start in nbu.prange(CORES):
        for i in range(start, size, CORES):
            out[i] = func(arr[i][0], arr[i][1])


def fromArray2D1D(arr: np.ndarray, out: np.ndarray, func) -> None:
    size = arr.shape[0]
    for start in nbu.prange(CORES):
        for i in range(start, size, CORES):
            out[i] = func(arr[i][0])


def fromArray1D(arr: np.ndarray, out: np.ndarray, func) -> None:
    size = arr.shape[0]
    for start in nbu.prange(CORES):
        for i in range(start, size, CORES):
            out[i] = func(arr[i])


def _not_init(*args, **kwargs) -> None:
    print(f"""perlin noise module not initialized""", file=sys.stderr)


class PerlinNoise:
    __call__ = staticmethod(
        functools.wraps(noise3D)(_not_init)
    )  # this is how you decorate a function without the @
    noise3D = staticmethod(functools.wraps(noise3D)(_not_init))
    noise2D = staticmethod(functools.wraps(noise2D)(_not_init))
    noise1D = staticmethod(functools.wraps(noise1D)(_not_init))
    detail = staticmethod(functools.wraps(_noise_detail)(_not_init))
    set_seed = staticmethod(functools.wraps(_set_seed)(_not_init))

    _fromArrayFuncs: dict = {}
    from_array = staticmethod(functools.wraps(fromArray)(_not_init))

    @classmethod
    def init(cls) -> int:
        """
        it initializes the noise module
        :return: int
        """
        try:
            global _perlin

            _perlin = np.random.random((_PERLIN_SIZE + 1,))

            cls.__call__ = staticmethod(nbu.njit(func=noise3D))
            cls.noise3D = staticmethod(nbu.njit(func=noise3D))
            cls.noise2D = staticmethod(nbu.njit(func=noise2D))
            cls.noise1D = staticmethod(nbu.njit(func=noise1D))
            cls.detail = classmethod(_noise_detail)
            cls.set_seed = classmethod(_set_seed)

            cls._fromArrayFuncs = {
                1: nbu.njit(nosig=True, func=fromArray2D1D, nogil=False, parallel=True),
                2: nbu.njit(nosig=True, func=fromArray2D2D, nogil=False, parallel=True),
                3: nbu.njit(nosig=True, func=fromArray2D3D, nogil=False, parallel=True),
            }

            cls.from_array = classmethod(fromArray)

            return 0
        except Exception as e:
            print(
                f"""unable to load perlin noise due to {str(type(e)).split("'")[~1]} -> {e}""",
                file=sys.stderr,
            )
            return 1

    @classmethod
    def quit(cls) -> int:
        """
        it uninitializes the perlin noise module
        :return: int
        """
        try:
            global _perlin

            cls.__call__ = staticmethod(functools.wraps(noise3D)(_not_init))
            cls.noise3D = staticmethod(functools.wraps(noise3D)(_not_init))
            cls.noise2D = staticmethod(functools.wraps(noise2D)(_not_init))
            cls.noise1D = staticmethod(functools.wraps(noise1D)(_not_init))
            cls.detail = staticmethod(functools.wraps(_noise_detail)(_not_init))
            cls.set_seed = staticmethod(functools.wraps(_set_seed)(_not_init))
            _perlin = None

            cls._fromArrayFuncs: dict = {}
            cls.from_array = staticmethod(functools.wraps(fromArray)(_not_init))

            return 0
        except Exception as e:
            print(
                f"""unable to unload perlin noise due to {str(type(e)).split("'")[~1]} -> {str(type(e)).split("'")[~1]}: {e}""",
                sys.stderr,
            )
            return 1


noise = PerlinNoise()
