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
some drawing functions
"""

from typing import List, Union, Tuple, Sequence, Optional, Dict
import PygameHaze.utils._numba_utils as nbu
from PygameHaze.utils.formulas import *
from PygameHaze.exceptions import *
from PygameHaze.constants import *
from PygameHaze.types import *

import pygame.gfxdraw
import numpy as np
import pygame

import os

CORES = os.cpu_count()
_ARRAY_MEMORY: Dict[int, np.ndarray] = {}


@nbu.njit(parallel=True)
def _cubic_bezier_points(
        pt1: nbu.Array(float, 1),
        pt2: nbu.Array(float, 1),
        pt3: nbu.Array(float, 1),
        pt4: nbu.Array(float, 1),
        quality: int,
        out: nbu.Array(float, 2)
) -> None:
    for start in nbu.prange(CORES):
        for i in range(start, quality + 1, CORES):
            t = i / quality
            t3 = t ** 3
            t2 = t ** 2
            out[i] = pt1 * (-t3 + 3 * t2 - 3 * t + 1) +\
                     pt2 * (3 * t3 - 6 * t2 + 3 * t) +\
                     pt3 * (-3 * t3 + 3 * t2) +\
                     pt4 * t3


@nbu.njit(parallel=True)
def _quadratic_bezier_points(
        pt1: nbu.Array(float, 1),
        pt2: nbu.Array(float, 1),
        pt3: nbu.Array(float, 1),
        quality: int,
        out: nbu.Array(float, 2)
) -> None:
    for start in nbu.prange(CORES):
        for i in range(start, quality + 1, CORES):
            t = i / quality
            out[i] = (
                lerp(lerp(pt1[0], pt2[0], t), lerp(pt2[0], pt3[0], t), t),
                lerp(lerp(pt1[1], pt2[1], t), lerp(pt2[1], pt3[1], t), t)
            )


# some of this functions are in classes for better organisation


_MISSING = object()


class _SO:  # shared object for convenience
    vertexes_list: List[List[Tuple[int, int]]] = []
    surfaces: List[Optional[pygame.surface.Surface]] = []
    loc_00: pygame.math.Vector2 = pygame.math.Vector2()
    list_prev_00: List[pygame.math.Vector2] = []


class Curves:
    @classmethod
    def quadratic_bezier(
            cls,
            surface: pygame.surface.Surface,
            p1: CoordsType,
            p2: CoordsType,
            p3: CoordsType,
            quality: int=1000,
            color: ColorType=WHITE,
            width: int=1
    ) -> pygame.Rect:
        """
        it creates a bezier curve based on 3 points (1 static, 1 control points an 1 static) aka a quadratic bezier
        :param surface: pygame.surface.Surface
        :param p1: the first point
        :param p2: the second point
        :param p3: the third point
        :param quality: the amount of points that will be used
        :param color: the color that it will be drawn as
        :param width: the width of teh curve
        :type surface: pygame.surface.Surface
        :type p1: CoordsType
        :type p2: CoordsType
        :type p3: CoordsType
        :type quality: Union[int, float]
        :type color: ColorType
        :type width: int
        :return: pygame.Rect
        """
        quality = int(quality)
        if quality not in _ARRAY_MEMORY:
            _ARRAY_MEMORY[quality] = np.zeros((quality, 2))
        points = _ARRAY_MEMORY[quality]
        _quadratic_bezier_points(np.array(p1), np.array(p2), np.array(p3), quality, points)
        return Draw.lines(
            surface,
            color,
            False,
            points,
            width
        )

    @classmethod
    def bezier(
            cls,
            surface: pygame.surface.Surface,
            p1: CoordsType,
            p2: CoordsType,
            p3: CoordsType,
            p4: CoordsType,
            quality: int=100,
            color: ColorType=WHITE,
            width: int=1
    ) -> pygame.Rect:
        """
        it creates a bezier curve based on 4 points (1 static, 2 control points an 1 static) aka a cubic bezier
        :param surface: pygame.surface.Surface
        :param p1: the first point
        :param p2: the second point
        :param p3: the third point
        :param p4: the fourth point
        :param quality: the amount of points that will be used
        :param color: the color that it will be drawn as
        :param width: the width of teh curve
        :type surface: pygame.surface.Surface
        :type p1: CoordsType
        :type p2: CoordsType
        :type p3: CoordsType
        :type p4: CoordsType
        :type quality: Union[int, float]
        :type color: ColorType
        :type width: int
        :return: pygame.Rect
        """
        quality = int(quality)
        if quality not in _ARRAY_MEMORY:
            _ARRAY_MEMORY[quality] = np.zeros((quality, 2))
        points = _ARRAY_MEMORY[quality]
        _cubic_bezier_points(np.array(p1), np.array(p2), np.array(p3), np.array(p4), quality, points)
        return Draw.lines(
            surface,
            color,
            False,
            points,
            width
        )


class Draw:
    bezier = Curves.bezier
    quadratic_bezier = Curves.quadratic_bezier

    @staticmethod
    def push() -> None:
        """
        it saves the current 0, 0 location for drawing
        :return: None
        """
        _SO.list_prev_00.append(pygame.math.Vector2(_SO.loc_00))

    @staticmethod
    def translate(
        x: Union[Number, pygame.math.Vector2, Tuple[Number, Number], List[Number]],
        y: Optional[Number]=_MISSING
    ) -> None:
        """
        it sets the 0, 0 position for drawing
        :param x: Optional[Union[Number, pygame.math.Vector2, Vector, Tuple[Number, Number], List[Number]]]
        :param y: Optional[Number]
        :return:
        """
        if y is _MISSING or y is None:
            if not isinstance(x, (int, float)):
                x, y = x
            else:
                y = x
        _SO.loc_00.x = x
        _SO.loc_00.y = y

    @staticmethod
    def pop() -> None:
        """
        it gets the old 0, 0 location for drawing
        :return: None
        """
        if not len(_SO.list_prev_00):
            raise NoLocationFound("tried to 'pop' without having 'pushed' any values")
        _SO.loc_00 = pygame.math.Vector2(_SO.list_prev_00.pop())

    @staticmethod
    def beginShape(surface: pygame.surface.Surface) -> None:
        """
        begins recording vertices for a shape
        :param surface: pygame.surface.Surface
        :return: None
        """
        _SO.vertexes_list.append([])
        _SO.surfaces.append(surface)

    @staticmethod
    def vertex(
        x: Union[Number, pygame.math.Vector2, Tuple[Number, Number], List[Number]],
        y: Optional[Number]=_MISSING
    ) -> None:
        """
        specify the vertex coordinates for the shapes
        :param x: Optional[Union[Number, pygame.math.Vector2, Vector, Tuple[Number, Number], List[Number]]]
        :param y: Optional[Number]
        :return:
        """
        if y is _MISSING or y is None:
            if not isinstance(x, (int, float)):
                x, y = x
            else:
                y = x
        _SO.vertexes_list[~0].append((int(x), int(y)))

    @staticmethod
    def endShape(
            closed: Optional[Union[int, bool]]=None,
            fill: Optional[Union[int, bool]]=None,
            color: ColorType=(255, 255, 255),
            width: int=1,
            outline: Optional[int]=0,
            outline_color: ColorType=BLACK
    ) -> pygame.Rect:
        """
        it ends the shape and draws the shape that was constructed by the beginShape and vertex
        :param closed: Optional[Union[int, bool]]=None
        :param fill: Optional[Union[int, bool]]=None
        :param color: ColorType=(255, 255, 255)
        :param width: int=1
        :param outline: Optional[int]=0
        :param outline_color: Optional[ColorType]
        :return: pygame.Rect
        """
        if not len(_SO.surfaces):
            raise ShapeError("shape was never started. start a shape with PygameHaze.beginShape")
        if fill:
            xx = sorted([v[0] for v in _SO.vertexes_list[~0]])
            yy = sorted([v[1] for v in _SO.vertexes_list[~0]])
            min_x = xx[0]
            max_x = xx[~0]
            min_y = yy[0]
            max_y = yy[~0]
            w = int(max_x - min_x)
            h = int(max_y - min_y)
            surf = pygame.surface.Surface((w, h))
            if color[0] >= 255: surf.fill((0, color[1], color[2])); surf.set_colorkey((0, color[1], color[2]))
            else: surf.fill((255, color[1], color[2])); surf.set_colorkey((255, color[1], color[2]))
            pygame.draw.polygon(surf, color, [(p[0] + abs(min_x), p[1] + abs(min_y)) for p in _SO.vertexes_list[~0]])
            r = _SO.surfaces[~0].blit(surf, (_SO.loc_00.x, _SO.loc_00.y))
        else:
            r = Draw.lines(_SO.surfaces[~0], color, closed, _SO.vertexes_list[~0], width)
        if outline: Draw.lines(_SO.surfaces[~0], outline_color, closed, _SO.vertexes_list[~0], outline)
        _SO.vertexes_list.pop()
        _SO.surfaces.pop()
        return r

    @staticmethod
    def rect(
            surface: pygame.surface.Surface,
            color: ColorType,
            rect: RectType,
            width: Optional[int]=0,
            border_radius: Optional[int]=-1,
            border_top_left_radius: Optional[int]=-1,
            border_top_right_radius: Optional[int]=-1,
            border_bottom_left_radius: Optional[int]=-1,
            border_bottom_right_radius: Optional[int]=-1
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.rect but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param rect: RectType
        :param width: Optional[int]=0
        :param border_radius: Optional[int]=-1
        :param border_top_left_radius: Optional[int]=-1
        :param border_top_right_radius: Optional[int]=-1
        :param border_bottom_left_radius: Optional[int]=-1
        :param border_bottom_right_radius: Optional[int]=-1
        :return: pygame.Rect
        """
        rect = pygame.Rect(rect)
        rect.x += _SO.loc_00.x
        rect.y += _SO.loc_00.y
        return pygame.draw.rect(
            surface,
            color,
            rect,
            width,
            border_radius,
            border_top_left_radius,
            border_top_right_radius,
            border_bottom_left_radius,
            border_bottom_right_radius
        )

    @staticmethod
    def polygon(
        surface: pygame.surface.Surface,
        color: ColorType,
        points: Sequence[CoordsType],
        width: Optional[int]=0
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.polygon but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param points: Sequence[CoordsType]
        :param width: Optional[int]=0
        :return: pygame.Rect
        """
        return pygame.draw.polygon(
            surface,
            color,
            list(map(lambda pos: (pos[0] + _SO.loc_00.x, pos[1] + _SO.loc_00.y), points)),
            width
        )

    @staticmethod
    def circle(
            surface: pygame.surface.Surface,
            color: ColorType,
            center: CoordsType,
            radius: float,
            width: Optional[int] = 0,
            draw_top_right: bool=False,
            draw_top_left: bool=False,
            draw_bottom_left: bool=False,
            draw_bottom_right: bool=False
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.circle but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param center: CoordsType
        :param radius: float
        :param width: Optional[int] = 0
        :param draw_top_right: Optional[bool]=None
        :param draw_top_left: Optional[bool]=None
        :param draw_bottom_left: Optional[bool]=None
        :param draw_bottom_right: Optional[bool]=None
        :return: pygame.Rect
        """
        return pygame.draw.circle(
            surface,
            color,
            (center[0] + _SO.loc_00.x, center[1] + _SO.loc_00.y),
            radius,
            width,
            draw_top_right,
            draw_top_left,
            draw_bottom_left,
            draw_bottom_right
        )

    @staticmethod
    def ellipse(
        surface: pygame.surface.Surface,
        color: ColorType,
        rect: RectType,
        width: Optional[int] = 0
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.ellipse but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param rect: RectType
        :param width: Optional[int]=0
        :return: pygame.Rect
        """
        rect = pygame.Rect(rect)
        rect.x += _SO.loc_00.x
        rect.y += _SO.loc_00.y
        return pygame.draw.ellipse(
            surface,
            color,
            rect,
            width
        )

    @staticmethod
    def arc(
            surface: pygame.surface.Surface,
            color: ColorType,
            rect: RectType,
            start_angle: float,
            stop_angle: float,
            width: Optional[int]=1
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.arc but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param rect: RectType
        :param start_angle: float
        :param stop_angle: float
        :param width: Optional[int] = 1
        :return: pygame.Rect
        """
        rect = pygame.Rect(rect)
        rect.x += _SO.loc_00.x
        rect.y += _SO.loc_00.y
        return pygame.draw.arc(
            surface,
            color,
            rect,
            start_angle,
            stop_angle,
            width
        )

    @staticmethod
    def line(
        surface: pygame.surface.Surface,
        color: ColorType,
        start_pos: CoordsType,
        end_pos: CoordsType,
        width: Optional[int]=1,
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.line but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param start_pos: CoordsType
        :param end_pos: CoordsType
        :param width: Optional[int]=1
        :return: pygame.Rect
        """
        start_pos = (start_pos[0] + _SO.loc_00.x, start_pos[1] + _SO.loc_00.y)
        end_pos = (end_pos[0] + _SO.loc_00.x, end_pos[1] + _SO.loc_00.y)
        return pygame.draw.line(
            surface,
            color,
            start_pos,
            end_pos,
            width
        )

    @staticmethod
    def lines(
            surface: pygame.surface.Surface,
            color: ColorType,
            closed: bool,
            points: Sequence[CoordsType],
            width: Optional[int] = 1,
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.lines but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param closed: bool
        :param points: Sequence[CoordsType]
        :param width: Optional[int] = 1
        :return: pygame.Rect
        """
        return pygame.draw.lines(
            surface,
            color,
            closed,
            list(map(lambda pos: (pos[0] + _SO.loc_00.x, pos[1] + _SO.loc_00.y), points)),
            width
        )

    @staticmethod
    def aaline(
            surface: pygame.surface.Surface,
            color: ColorType,
            start_pos: CoordsType,
            end_pos: CoordsType,
            blend: Optional[int] = 1,
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.aaline but it utilises the translated value
        :param surface: pygame.surface.Surface,
        :param color: ColorType,
        :param start_pos: CoordsType,
        :param end_pos: CoordsType,
        :param blend: Optional[int] = 1,
        :return: pygame.Rect
        """
        start_pos = (start_pos[0] + _SO.loc_00.x, start_pos[1] + _SO.loc_00.y)
        end_pos = (end_pos[0] + _SO.loc_00.x, end_pos[1] + _SO.loc_00.y)
        return pygame.draw.line(
            surface,
            color,
            start_pos,
            end_pos,
            blend
        )

    @staticmethod
    def aalines(
            surface: pygame.surface.Surface,
            color: ColorType,
            closed: bool,
            points: Sequence[CoordsType],
            blend: Optional[int] = 1,
    ) -> pygame.Rect:
        """
        a wrapper for pygame.draw.aalines but it utilises the translated value
        :param surface: pygame.surface.Surface
        :param color: ColorType
        :param closed: bool
        :param points: Sequence[CoordsType]
        :param blend: Optional[int] = 1
        :return: pygame.Rect
        """
        return pygame.draw.aalines(
            surface,
            color,
            closed,
            list(map(lambda pos: (pos[0] + _SO.loc_00.x, pos[1] + _SO.loc_00.y), points)),
            blend
        )


draw = Draw  # i like having classes capitalized but the draw to keep it similar to pygame


def build_draw_numba():
    _quadratic_bezier_points(
        np.array([0, 0]), np.array([1, 1]), np.array([2, 0]),
        10, np.ndarray((10, 2))
    )
    _cubic_bezier_points(
        np.array([0, 1]), np.array([1, 2]), np.array([2, -1]), np.array([3, 1]),
        10, np.ndarray((10, 2))
    )


__all__ = [
    "draw", "Draw"
]
