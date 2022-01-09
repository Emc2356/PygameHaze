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
a cloth object made with verlet integration
"""


from typing import Tuple, List, Union, Dict
import math
import pygame

from PygameHazel.exceptions import *


class Cloth:
    """
    Creates a cloth object

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that the cloth is going to be rendered in
    x: int
        the x position of the cloth
    y: int
        the y position of the cloth
    data: Dict[str, list]
        the information that the cloth is going to be generated in

    Methods:
    -----------
    update(dt=1):
        it updates the cloth
    move_locked(pos):
        it moves the locked points in a given position (they keep their offsets)
    move_all(pos):
        it moves all of the points in a given position (they keep their offsets)
    offset_locked(pos):
        it moves the locked points by a given offset
    offset_all(pos):
        it moves all of the points by a given offset
    draw(color, filled=False, width=2):
        it draws the cloth
    """
    def __init__(self, WIN: pygame.surface.Surface, data: Dict[str, list]):
        self._data: dict = data.copy()
        self.WIN: pygame.surface.Surface = WIN
        self.W, self.H = self.WIN.get_size()

        self.points: List[Point] = Point.load_list(data["points"])
        if not any([p.locked for p in self.points]):
            raise NoLockedPoints("the given cloth has no locked points")
        self.connections: List[Connection] = [Connection(self.points[cn[0]], self.points[cn[1]], cn[2]) for cn in data["connections"]]

    def update(self, dt: Union[int, float]=1) -> None:
        """
        it moves the points
        :param dt: Union[int, float]
        :return: None
        """
        for point in self.points:
            point.update(dt)
        for _ in range(10):
            for con in self.connections:
                con.update(dt)

    def collide(self, rects: List[pygame.Rect]) -> None:
        raise Notimplemented("collide method for cloth object is not implemented yet.")
        rects = [pygame.Rect(r) for r in rects]
        for point in self.points:
            for rect in rects:
                r = pygame.Rect(rect.x + 1, rect.y + 1, rect.w - 2, rect.h - 2)
                if point.locked or not r.collidepoint(*point.pos):
                    continue
                dx = point.pos.x - point.prev_pos.x
                dy = point.pos.y - point.prev_pos.y
                if dx:
                    if dx > 0:  # right
                        point.pos.x = rect.left
                        point.prev_pos.x = point.pos.x + dx
                    else:  # left
                        point.pos.x = rect.right
                        point.prev_pos.x = point.pos.x + dx
                if dy:
                    if dy > 0:  # down
                        point.pos.y = rect.top
                        point.prev_pos.y = point.pos.y + dy
                    else:  # up
                        point.pos.y = rect.bottom
                        point.prev_pos.y = point.pos.y + dy
                break
        del rects

    def borders(self) -> None:
        """
        it keeps the points inside the window that is passed when the class is initialized
        :return: None
        """
        for point in self.points:
            dx = point.pos.x - point.prev_pos.x
            dy = point.pos.y - point.prev_pos.y
            if point.pos.x > self.W:
                point.pos.x = self.W
                point.prev_pos.x = point.pos.x + dx

            elif point.pos.x < 0:
                point.pos.x = 0
                point.prev_pos.x = point.pos.x + dx

            if point.pos.y > self.H:
                point.pos.y = self.H
                point.prev_pos.y = point.pos.y + dy

            elif point.pos.y < 0:
                point.pos.y = 0
                point.prev_pos.y = point.pos.y + dy

    def move_locked(self, pos: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]) -> None:
        """
        it moves all of the locked locations the velocities of the "free" points are going to change
        :param pos: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]
        :return: None
        """
        difference = [
            pos[0] - min([point.pos.x for point in self.points if point.locked], default=0),
            pos[1] - min([point.pos.y for point in self.points if point.locked], default=0)
        ]
        for point in self.points:
            if point.locked:
                point.pos += difference
                point.prev_pos += difference

    def move_all(self, pos: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]) -> None:
        """
        it moves the cloth with a given offset the velocities are the same they are not effected
        :param pos: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]
        :return: None
        """
        difference = [
            pos[0] - min([point.pos.x for point in self.points if point.locked], default=0),
            pos[1] - min([point.pos.y for point in self.points if point.locked], default=0)
        ]
        for point in self.points:
            point.pos += difference
            point.prev_pos += difference

    def offset_locked(self, offset: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]) -> None:
        """
        it moves all of the locked points in a cloth by a given amount velocities will not be effected
        :param offset: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]
        :return: None
        """
        for point in self.points:
            if point.locked:
                point.pos += offset
                point.prev_pos += offset

    def offset_all(self, offset: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]) -> None:
        """
        it moves all of the points in a cloth by a given amount velocities will not be effected
        :param offset: Union[Tuple[Union[int, float], Union[int, float]], List[Union[int, float]], pygame.math.Vector2]
        :return: None
        """
        for point in self.points:
            point.pos += offset
            point.prev_pos += offset

    def draw(self, color: Tuple[int, int, int] or Tuple[int, int, int, int], filled: bool=False, width: int=2):
        for con in self.connections:
            pygame.draw.line(self.WIN, color, con.pointA.pos, con.pointB.pos, width)

    @staticmethod
    def load(WIN: pygame.surface.Surface, data: List[Dict[str, list]]) -> "Cloth":
        return Cloth(WIN, *data)

    @staticmethod
    def save(cloth: "Cloth") -> List[Dict[str, list]]:
        return [cloth._data]


class Point:
    def __init__(self, x: int, y: int, locked: bool, gravity: Union[int, float]=0.2):
        self.locked: bool = locked
        self.gravity: Union[int, float] = gravity
        self.pos: pygame.math.Vector2 = pygame.math.Vector2(x, y)
        self.prev_pos: pygame.math.Vector2 = pygame.math.Vector2(x, y)
        self.friction: Union[int, float] = 0.999

    def update(self, dt: Union[int, float]=1) -> None:
        if not self.locked:
            dx = (self.pos.x - self.prev_pos.x) * self.friction
            dy = (self.pos.y - self.prev_pos.y) * self.friction
            self.prev_pos.x, self.prev_pos.y = self.pos.x, self.pos.y
            self.pos.x += dx * dt
            self.pos.y += (dy + self.gravity) * dt

    @staticmethod
    def save(point: "Point") -> List[Union[Union[int, float], Union[int, float], bool, Union[int, float]]]:
        return [point.pos.x, point.pos.y, point.locked, point.gravity]

    @staticmethod
    def load(data: List[Union[Union[int, float], Union[int, float], bool, Union[int, float]]]) -> "Point":
        return Point(*data)

    @staticmethod
    def load_list(dts: List[List[Union[Union[int, float], Union[int, float], bool, Union[int, float]]]]) -> List["Point"]:
        return [Point.load(data) for data in dts]


class Connection:
    def __init__(self, pointA: Point, pointB: Point, length: Union[int, float]):
        self.pointA: Point = pointA
        self.pointB: Point = pointB
        self.length: Union[int, float] = length

    def update(self, dt: Union[int, float]=1) -> None:
        dx = self.pointB.pos.x - self.pointA.pos.x
        dy = self.pointB.pos.y - self.pointA.pos.y
        distance = math.sqrt(dx * dx + dy * dy)
        difference = self.length - distance
        percent = difference / distance / 2
        offset = [dx * percent, dy * percent]
        if not self.pointA.locked:
            self.pointA.pos.x -= offset[0] * dt
            self.pointA.pos.y -= offset[1] * dt
        if not self.pointB.locked:
            self.pointB.pos.x += offset[0] * dt
            self.pointB.pos.y += offset[1] * dt

    @staticmethod
    def save(con: "Connection", points: List[Point]) -> List[Union[int, int, Union[int, float]]]:
        return [points.index(con.pointA), points.index(con.pointB), con.length]

    @staticmethod
    def load(data: List[Union[int, int, Union[int, float]]], points) -> "Connection":
        return Connection(points[data[0]], points[data[1]], data[2])
