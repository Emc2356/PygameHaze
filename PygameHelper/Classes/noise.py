from typing import Union
import random
import numpy
import math


NumType = Union[int, float]


class _Noise:
    _PERLIN_YWRAPB = 4
    _PERLIN_YWRAP = 1 << _PERLIN_YWRAPB
    _PERLIN_ZWRAPB = 8
    _PERLIN_ZWRAP = 1 << _PERLIN_ZWRAPB
    _PERLIN_SIZE = 4095
    _perlin_octaves = 4  # default to medium smooth
    _perlin_amp_falloff = 0.5  # 50% reduction/octave
    _perlin = None

    @staticmethod
    def _scaled_cosine(i: NumType) -> NumType:
        return 0.5 * (1.0 - math.cos(i * math.pi))

    def __call__(self, x: NumType, y: NumType=0, z: NumType=0) -> NumType:
        if self._perlin is None:
            self._perlin = numpy.ndarray([self._PERLIN_SIZE + 1])
            for i in range(self._PERLIN_SIZE):
                self._perlin[i] = random.random()

        if x < 0: x = -x
        if y < 0: y = -y
        if z < 0: z = -z

        xi = math.floor(x)
        yi = math.floor(y)
        zi = math.floor(z)
        xf = x - xi
        yf = y - yi
        zf = z - zi

        r = 0
        ampl = 0.5

        for o in range(self._perlin_octaves):
            of = xi + (yi << self._PERLIN_YWRAPB) + (zi << self._PERLIN_ZWRAPB)

            rxf = self._scaled_cosine(xf)
            ryf = self._scaled_cosine(yf)

            n1 = self._perlin[of & self._PERLIN_SIZE]
            n1 += rxf * (self._perlin[(of + 1) & self._PERLIN_SIZE] - n1)
            n2 = self._perlin[(of + self._PERLIN_YWRAP) & self._PERLIN_SIZE]
            n2 += rxf * (self._perlin[(of + self._PERLIN_YWRAP + 1) & self._PERLIN_SIZE] - n2)
            n1 += ryf * (n2 - n1)

            of += self._PERLIN_ZWRAP
            n2 = self._perlin[of & self._PERLIN_SIZE]
            n2 += rxf * (self._perlin[(of + 1) & self._PERLIN_SIZE] - n2)
            n3 = self._perlin[(of + self._PERLIN_YWRAP) & self._PERLIN_SIZE]
            n3 += rxf * (self._perlin[(of + self._PERLIN_YWRAP + 1) & self._PERLIN_SIZE] - n3)
            n2 += ryf * (n3 - n2)

            n1 += self._scaled_cosine(zf) * (n2 - n1)

            r += n1 * ampl
            ampl *= self._perlin_amp_falloff
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

        return r


noise = _Noise()
