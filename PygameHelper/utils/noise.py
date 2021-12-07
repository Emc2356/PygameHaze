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

from typing import Optional, Dict
import numpy as np
import numba as nb
import functools
import random
import math


_PERLIN_YWRAPB: int = 4
_PERLIN_YWRAP: int = 1 << _PERLIN_YWRAPB
_PERLIN_ZWRAPB: int = 8
_PERLIN_ZWRAP: int = 1 << _PERLIN_ZWRAPB
_PERLIN_SIZE: int = 4095
_octaves: int = 4  # default to medium smooth
_perlin_amp_falloff: float = 0.5  # 50% reduction/octave
_perlin: Optional[np.ndarray] = None  # lazy load it


class float64(float): pass
class float32(float): pass
class int64(int): pass
class int32(int): pass


TYPES: Dict[type, str] = {
    float64: "float64",
    float32: "float32",
    float: "float64",
    int64: "int64",
    int32: "int32",
    int: "int64"
}


def construct_sig(func) -> Optional[str]:
    # constructing a numba signature out of the typehints of the function
    if hasattr(func, "__annotations__") and func.__annotations__:
        args, ret = [], []
        for name, anno in func.__annotations__.items():
            if name != "return": args.append((name, anno))
            else: ret.append(anno)
        return f"""{TYPES.get(ret[0], ret[0])}({", ".join([TYPES.get(anno, anno) for name, anno in args])})"""
    return None


def njit(sig=None, **kwargs):
    if sig is None:
        sig = construct_sig(kwargs.get("func", None))

    if sig is not None:
        if "func" in kwargs:
            func = kwargs.pop("func")
            return nb.njit(sig, fastmath=kwargs.get("fastmath", True), nogil=kwargs.get("nogil", True), **kwargs)(func)
        return nb.njit(sig, fastmath=kwargs.get("fastmath", True), nogil=kwargs.get("nogil", True), **kwargs)
    if "func" in kwargs:
        func = kwargs.pop("func")
        return nb.njit(fastmath=kwargs.get("fastmath", True), nogil=kwargs.get("nogil", True), **kwargs)(func)
    return nb.njit(fastmath=kwargs.get("fastmath", True), nogil=kwargs.get("nogil", True), **kwargs)


def set_seed(seed: int) -> None:
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


def _noise_detail(octaves: int=-1, falloff: float=-1) -> None:
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


@njit("float64(float64)")
def _scaled_cosine(i: float) -> float:
    return 0.5 * (1.0 - math.cos(i * math.pi))


def noise3DPurePython(x: float, y: float=0, z: float=0) -> float:
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


def noise2DPurePython(x: float, y: float=0) -> float:
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


def noise1DPurePython(x: float) -> float:
    """
    it calculates the 2D perlin noise value based on the random values and the values passed
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


def _not_init(*args, **kwargs) -> None:
    from colorama import (
        Fore,
        Style
    )
    print(f"""{Fore.RED}perlin noise module not initialized{Style.RESET_ALL}""")


class PerlinNoise:
    __call__ = staticmethod(functools.wraps(noise3DPurePython)(_not_init))  # this is how you decorate a function without the @
    noise3D  = staticmethod(functools.wraps(noise3DPurePython)(_not_init))
    noise2D  = staticmethod(functools.wraps(noise2DPurePython)(_not_init))
    noise1D  = staticmethod(functools.wraps(noise1DPurePython)(_not_init))
    detail   = staticmethod(functools.wraps(_noise_detail)(_not_init))
    set_seed = staticmethod(functools.wraps(set_seed)(_not_init))

    @classmethod
    def init(cls) -> int:
        """
        it initializes the noise module
        :return: int
        """
        try:
            global _perlin

            _perlin = np.random.random((_PERLIN_SIZE + 1,))

            cls.__call__ = staticmethod(njit(func=noise3DPurePython))
            cls.noise3D  = staticmethod(njit(func=noise3DPurePython))
            cls.noise2D  = staticmethod(njit(func=noise2DPurePython))
            cls.noise1D  = staticmethod(njit(func=noise1DPurePython))
            cls.detail   = staticmethod(_noise_detail)
            cls.set_seed = staticmethod(set_seed)
            return 0
        except Exception as e:
            from colorama import (
                Fore,
                Style
            )
            print(f"""{Fore.RED}unable to load perlin noise due to {str(type(e)).split("'")[~1]} -> {str(type(e)).split("'")[~1]}: {e}{Style.RESET_ALL}""")
            return 1

    @classmethod
    def quit(cls) -> int:
        """
        it uninitializes the perlin noise module
        :return: int
        """
        try:
            global _perlin

            cls.__call__ = staticmethod(functools.wraps(noise3DPurePython)(_not_init))
            cls.noise3D  = staticmethod(functools.wraps(noise3DPurePython)(_not_init))
            cls.noise2D  = staticmethod(functools.wraps(noise2DPurePython)(_not_init))
            cls.noise1D  = staticmethod(functools.wraps(noise1DPurePython)(_not_init))
            cls.detail   = staticmethod(functools.wraps(_noise_detail)(_not_init))
            cls.set_seed = staticmethod(functools.wraps(set_seed)(_not_init))
            _perlin = None
            return 0
        except Exception as e:
            from colorama import (
                Fore,
                Style
            )
            print(f"""{Fore.RED}unable to unload perlin noise due to {str(type(e)).split("'")[~1]} -> {str(type(e)).split("'")[~1]}: {e}{Style.RESET_ALL}""")
            return 1


noise = PerlinNoise()
