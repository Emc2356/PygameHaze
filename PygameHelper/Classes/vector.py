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
a Vector like pygame.math.Vector2 but with some extra functionality (i think so)
"""


from typing import List, Tuple, Union, Optional, Iterable, overload as TpOverload, Sequence

import pygame
import random
import math


_MISSING = object()
NumTyp = Union[int, float]
NumTup = (int, float)


class Vector:
    """
    Vector object

    Parameters:
    -----------
    x: Optional[Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]]]=0
        the x component
    y: Optional[float]=0
        the x component

    Methods:
    -----------
    add(x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING):
        it adds a value to the Vector
    sub(x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING):
        it subtracts a value to the Vector
    mul(x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING):
        it multiplies a value to the Vector
    div(x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING):
        it divides a value to the Vector
    dot(x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING):
        it calculates the dot product of two vectors
    cross(x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING):
        it returns the z value of the cross product from 2 Vectors
    lerp(x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING):
        linear interpolate between 2 Vectors
    distance(target: Union[pygame.math.Vector2, Vector, Tuple[Union[int, float], Union[int, float]], List[Union[int, float]]]):
        it calculates the Euclidean distance between two Vectors
    copy():
        it returns a copy of the vector
    tostring():
        it turns a Vector into string form
    @staticmethod
    fromstring(string: str):
        it returns a Vector from a string
    normalize():
        it normalizes the vector to length 1 (make it a unit vector)
    @property
    mag_sq
        it returns the magnitude of the vector squared
    @property
    mag
        it returns the magnitude of the vector
    @mag.setter
    mag = val
        it sets the magnitude of the vector
    set_mag(val: Union[int, float]):
        it sets the magnitude of the vector (same as instance.mag = value but it returns self to stack chain)
    limit(maxV: Union[int, flaot]):
        it limits the magnitude of the Vector
    rotate(angle: Union[int, float]):
        it rotates the vector in degrees or radians
    @property
    heading
        it calculate the angle of rotation for the vector
    @heading.setter
    heading = angle
        it sets the heading of the Vector (in degrees)
    from_angle(angle: Union[int, float], length: Union[int, float]=1, degrees=True):
        it makes a Vector from a given angle in degrees or radians
    @staticmethod
    random(length: Union[int, float]=1):
        it creates a random vector
    @staticmethod
    from_polar(r: Union[int, float], theta: Union[int, float], degrees=True):
        it creates a Vector from polar coordinates
    polar(r: Union[int, float], theta: Union[int, float], degrees=True):
        it sets the Vectors coordinates based on polar coordinates
    """
    __slots__ = "x", "y"

    def __init__(
            self,
            x: Optional[Union[NumTyp, pygame.math.Vector2, "Vector", Tuple[NumTyp, NumTyp], List[NumTyp]]]=0,
            y: Optional[NumTyp]=0,
    ) -> None:
        if not isinstance(x, (int, float)): x, y = x
        self.x: float = 0 if x is None else x
        self.y: float = 0 if y is None else y

    def add(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[float]=_MISSING,
    ) -> "Vector":
        """
        it adds a value to the Vector
        :param x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]]=0
        :param y: Optional[float]=0
        :return: Vector
        """
        if y is _MISSING or y is None:
            if not isinstance(x, (int, float)):
                x, y = x
            else:
                y = x
        self.x += x
        self.y += y
        return self

    def sub(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[float]=_MISSING,
    ) -> "Vector":
        """
        it subtracts a value to the Vector
        :param x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]]=0
        :param y: Optional[float]=0
        :return: Vector
        """
        if y is _MISSING or y is None:
            if not isinstance(x, (int, float)):
                x, y = x
            else:
                y = x
        self.x -= x
        self.y -= y
        return self

    def mul(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[float]=_MISSING,
    ) -> "Vector":
        """
        it multiplies a value to the Vector
        :param x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]]=0
        :param y: Optional[float]=0
        :return: Vector
        """
        if isinstance(x, (Vector, pygame.math.Vector2)):
            if (math.isfinite(x.x), math.isfinite(x.y)) and (isinstance(x.x, (int, float)), isinstance(x.y, (int, float))):
                self.x *= x.x
                self.y *= x.y
                return self
            else:
                raise TypeError("PygameHelper Vector mul method needs a finite number")
        if "__getitem__" in dir(x) or isinstance(x, (list, tuple)):
            if all([isinstance(el, (int, float)) and math.isfinite(el) for el in x]) and len(x) > 0:
                if len(x) == 1:
                    self.x *= x[0]
                    self.y *= x[0]
                elif len(x) > 1:
                    self.x *= x[0]
                    self.y *= x[1]
                return self
            else:
                raise TypeError("PygameHelper Vector mul method needs a finite number")
        args = [x]
        if y is not _MISSING: args.append(y)
        if all([isinstance(el, (int, float)) and math.isfinite(el) for el in args]):
            if len(args) == 1:
                self.x *= args[0]
                self.y *= args[0]
            else:
                self.x *= args[0]
                self.y *= args[1]
            return self
        else:
            raise TypeError("PygameHelper Vector mul method needs a finite number")

    def div(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[float]=_MISSING,
    ) -> "Vector":
        """
        it divides a value to the Vector
        :param x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]]=0
        :param y: Optional[float]=0
        :return: Vector
        """
        if isinstance(x, (Vector, pygame.math.Vector2)):
            if x.x == 0 or x.y == 0:
                raise ZeroDivisionError("PygameHelper Vector div method cant accept 0")
            if (math.isfinite(x.x), math.isfinite(x.y)) and (isinstance(x.x, (int, float)), isinstance(x.y, (int, float))):
                self.x /= x.x
                self.y /= x.y
                return self
            else:
                raise TypeError("PygameHelper Vector div method needs a finite number")
        if "__getitem__" in dir(x) or isinstance(x, (list, tuple)):
            if x[0] == 0 or x[1] == 0:
                raise ZeroDivisionError("PygameHelper Vector div method cant accept 0")
            if all([isinstance(el, (int, float)) and math.isfinite(el) for el in x]) and len(x) > 0:
                if len(x) == 1:
                    self.x /= x[0]
                    self.y /= x[0]
                elif len(x) > 1:
                    self.x /= x[0]
                    self.y /= x[1]
                return self
            else:
                raise TypeError("PygameHelper Vector div method needs a finite number")
        args = [x]
        if y is not _MISSING: args.append(y)
        if all([isinstance(el, (int, float)) and math.isfinite(el) for el in args]):
            if any([el == 0 for el in args]):
                raise ZeroDivisionError("PygameHelper Vector div method cant accept 0")
            if len(args) == 1:
                self.x /= args[0]
                self.y /= args[0]
            else:
                self.x /= args[0]
                self.y /= args[1]
            return self
        else:
            raise TypeError("PygameHelper Vector div method needs a finite number")

    def dot(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[Union[int, float]]=_MISSING
    ) -> float:
        """
        it calculates the dot product of two vectors
        :param x: Optional[Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]]]
        :param y: Optional[Union[int, float]]
        :return: float
        """
        if y is _MISSING or y is None:
            return self.dot(x[0], x[1])
        return self.x * x + self.y + y

    def cross(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[Union[int, float]]=_MISSING
    ) -> float:
        """
        it returns the z value of the cross product from 2 Vectors
        :return: float
        """
        if y is _MISSING or y is None:
            return self.cross(x[0], x[1])
        return self.x * y - self.y * x

    def lerp(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[Union[int, float]]=_MISSING,
            percent: float=0.5
    ) -> "Vector":
        """
        linear interpolate between 2 Vectors
        :param x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]],
        :param y: Optional[Union[int, float]]=_MISSING,
        :param percent: 0 <= float >= 1
        :return: Vector
        """
        if percent > 1 or percent < 0:
            if percent > 1:
                raise ValueError(f"percent in lerp method is bigger than 1")
            if percent < 0:
                raise ValueError(f"percent in lerp method is smaller than 0")
        if y is _MISSING or y is None:
            return self.lerp(x[0], x[1], percent)
        self.x += (x - self.x) * percent
        self.y += (y - self.y) * percent

        return self

    def distance(
            self,
            target: Union[pygame.math.Vector2, "Vector", Tuple[Union[int, float], Union[int, float]], List[Union[int, float]]]
    ) -> float:
        """
        it calculates the Euclidean distance between two Vectors
        :param target: Union[pygame.math.Vector2, "Vector", Tuple[Union[int, float], Union[int, float]], List[Union[int, float]]]
        :return: float
        """
        return math.sqrt(((self[0] - target[0]) ** 2 + (self[1] - target[1]) ** 2))

    def copy(self) -> "Vector":
        """
        it returns a copy of the vector
        :return: Vector
        """
        return Vector(self.x, self.y)

    def tostring(self) -> str:
        """
        it turns a Vector into string form
        :return: string
        """
        return f"Vector [${self.x} ${self.y}]"

    def __repr__(self) -> str:
        return f"Vector [${self.x} ${self.y}]"

    def __str__(self) -> str:
        return f"Vector [${self.x} ${self.y}]"

    @staticmethod
    def fromstring(string: str) -> "Vector":
        """
        it returns a Vector from a string
        :param string: str
        :return: Vector
        """
        return Vector([float(el) for el in string[:-1].split("$")[1:]])

    def normalize(self) -> "Vector":
        """
        it normalizes the vector to length 1 (make it a unit vector)
        :return: Vector
        """
        length = self.mag
        if length != 0: self.mul(1/length)
        return self

    @property
    def mag_sq(self) -> float:
        """
        it calculates the squared magnitude of the Vector
        :return: float
        """
        return self.x**2 + self.y**2

    @property
    def mag(self) -> float:
        """
        it returns the magnitude of the Vector
        :return: float
        """
        return math.sqrt(self.x**2 + self.y**2)

    @mag.setter
    def mag(self, val: Union[int, float]) -> None:
        self.normalize().mul(val)

    def set_mag(self, val: Union[int, float]) -> "Vector":
        """
        it sets the magnitude of the vector
        :param val: Union[int, float]
        :return: Vector
        """
        return self.normalize().mul(val)

    def limit(self, maxV: Union[int, float]) -> "Vector":
        """
        it limits the magnitude of the Vector
        :param maxV: Union[int, float]
        :return: Vector
        """
        mSq = self.mag_sq
        if mSq > maxV * maxV:
            self.div(math.sqrt(mSq)).mul(maxV)
        return self

    def rotate(self, angle: Union[int, float], degrees: bool=True) -> "Vector":
        """
        it rotates the vector in degrees or radians
        :param angle: Union[int, float]
        :param degrees: bool=True
        :return: Vector
        """
        m = self.mag
        if degrees: angle = math.radians(angle)
        self.x = m * math.cos(angle)
        self.y = m * math.sin(angle)
        return self

    @property
    def heading(self) -> float:
        """
        it calculate the angle of rotation for the vector
        :return: float
        """
        return math.degrees(math.atan2(self.y, self.x))

    @heading.setter
    def heading(self, angle: float) -> None:
        mag = self.mag
        self.x = mag * math.cos(math.radians(angle))
        self.y = mag * math.sin(math.radians(angle))

    @staticmethod
    def from_angle(angle: Union[int, float], length: Union[int, float]=1, degrees=True) -> "Vector":
        """
        it makes a Vector from a given angle in degrees or radians
        :param angle: Union[int, float]
        :param length: Union[int, float]
        :param degrees: True
        :return: Vector
        """
        if degrees:
            return Vector(length * math.cos(math.radians(angle)), length * math.sin(math.radians(angle)))
        return Vector(length * math.cos(angle), length * math.sin(angle))

    @staticmethod
    def random(length: Union[int, float]=1) -> "Vector":
        """
        it creates a random vector
        :param length: Union[int, float]
        :return: Vector
        """
        return Vector.from_angle(random.random() * math.pi*2, length)

    @staticmethod
    def from_polar(
            r: Union[int, float, List[NumTyp], Tuple[NumTyp], Sequence],
            theta: Optional[NumTyp]=_MISSING,
            degrees=True
    ) -> "Vector":
        """
        it generates a Vector from polar coordinates
        :param r: Union[int, float, List[NumTyp], Tuple[NumTyp], Sequence]
        :param theta: Optional[NumTyp]=None
        :param degrees: bool
        :return: Vector
        """
        if theta is _MISSING or theta is None:
            if isinstance(r, NumTup): raise TypeError(
                (f"theta is undefined and r isn't a Sequence of numbers |"
                 f" 'r' expected List or Tuple or Sequence but got '{type(r)}'")
            )
            r, theta, *_ = r
        if degrees:
            return Vector(r * math.cos(math.radians(theta)), r * math.sin(math.radians(theta)))
        return Vector(r * math.cos(theta), r * math.sin(theta))

    def polar(self, r: Union[int, float], theta: Union[int, float], degrees=True) -> "Vector":
        """
        it sets the Vectors coordinates based on polar coordinates
        :param r: Union[int, float]
        :param theta: Union[int, float]
        :param degrees: bool
        :return: Vector
        """
        if degrees:
            theta = math.radians(theta)
        self.x = r * math.cos(theta)
        self.y = r * math.sin(theta)
        return self

    def as_polar(self, degrees=True) -> Tuple[float, float]:
        """
        it returns a tuple with the polar coordinate representation of this Vector
        :param degrees: bool=True
        :return: Tuple[int, int]
        """
        h = self.mag
        return h, math.degrees(math.asin(self.y/h)) if degrees else math.asin(self.y/h)

    def update(
            self,
            x: Union[float, pygame.math.Vector2, "Vector", Tuple[float, float], List[float]],
            y: Optional[float]=_MISSING,
    ) -> "Vector":
        if y is _MISSING or y is None:
            if not isinstance(x, (int, float)):
                self.update(x[0], x[1])
            else:
                self.x = x
        else:
            if isinstance(y, (int, float)):
                if isinstance(x, (int, float)):
                    self.x = x
                    self.y = y
                else:
                    raise TypeError(f"x was expected to be an int or a float but got '{type(x)}'")
            else:
                raise TypeError(f"y was expected to be an int or a float but got '{type(x)}'")
        return self

    @TpOverload
    def __getitem__(self, index: int) -> int: ...

    @TpOverload
    def __getitem__(self, index: slice) -> List[int]: ...

    def __getitem__(self, index: Union[int, slice]) -> Union[float, List[float]]:
        return [self.x, self.y][index]

    def __len__(self) -> int:
        return 2

    def __iter__(self) -> Iterable:
        return iter([self.x, self.y])

    def __eq__(self, other: "Vector") -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other: "Vector") -> bool:
        return not (self.x == other.x and self.y == other.y)

    def __lt__(self, other: "Vector") -> bool:
        return self.mag < other.mag

    def __le__(self, other: "Vector") -> bool:
        return self.mag <= other.mag

    def __gt__(self, other: "Vector") -> bool:
        return self.mag > other.mag

    def __ge__(self, other: "Vector") -> bool:
        return self.mag >= other.mag
