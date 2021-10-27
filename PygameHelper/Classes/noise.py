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


from typing import Union
import random
import numpy as np
import math


NumType = Union[int, float]


class _PerlinNoise:
    def __init__(self):
        self.PERLIN_YWRAPB = 4
        self.PERLIN_YWRAP = 1 << self.PERLIN_YWRAPB
        self.PERLIN_ZWRAPB = 8
        self.PERLIN_ZWRAP = 1 << self.PERLIN_ZWRAPB
        self.PERLIN_SIZE = 4095
        self.octaves = 4  # default to medium smooth
        self.perlin_amp_falloff = 0.5  # 50% reduction/octave
        self.perlin = None

    def noise_detail(self, octaves: int=-1, falloff: float=-1) -> None:
        """
        its sets the number of octaves that are going to be used and the falloff factor for each octave
        :param octaves: int=-1
        :param falloff: int=-1
        :return:
        """
        if octaves > 0:
            self.octaves = octaves
        if falloff > 0:
            self.perlin_amp_falloff = falloff

    @staticmethod
    def _scaled_cosine(i: NumType) -> NumType:
        return 0.5 * (1.0 - math.cos(i * math.pi))

    def __call__(self, x: NumType, y: NumType=0, z: NumType=0) -> NumType:
        if self.perlin is None:
            self._perlin = np.ndarray([self.PERLIN_SIZE + 1])
            for i in range(self.PERLIN_SIZE + 1):
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

        for o in range(self.octaves):
            of = xi + (yi << self.PERLIN_YWRAPB) + (zi << self.PERLIN_ZWRAPB)

            rxf = self._scaled_cosine(xf)
            ryf = self._scaled_cosine(yf)

            n1 = self._perlin[of & self.PERLIN_SIZE]
            n1 += rxf * (self._perlin[(of + 1) & self.PERLIN_SIZE] - n1)
            n2 = self._perlin[(of + self.PERLIN_YWRAP) & self.PERLIN_SIZE]
            n2 += rxf * (self._perlin[(of + self.PERLIN_YWRAP + 1) & self.PERLIN_SIZE] - n2)
            n1 += ryf * (n2 - n1)

            of += self.PERLIN_ZWRAP
            n2 = self._perlin[of & self.PERLIN_SIZE]
            n2 += rxf * (self._perlin[(of + 1) & self.PERLIN_SIZE] - n2)
            n3 = self._perlin[(of + self.PERLIN_YWRAP) & self.PERLIN_SIZE]
            n3 += rxf * (self._perlin[(of + self.PERLIN_YWRAP + 1) & self.PERLIN_SIZE] - n3)
            n2 += ryf * (n3 - n2)

            n1 += self._scaled_cosine(zf) * (n2 - n1)

            r += n1 * ampl
            ampl *= self.perlin_amp_falloff
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


noise = _PerlinNoise()
