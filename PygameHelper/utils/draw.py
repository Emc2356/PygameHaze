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

from typing import List, Union, Tuple, Sequence, Optional
from PygameHelper.Classes.vector import Vector
from PygameHelper.utils.formulas import *
from PygameHelper.exceptions import *
from PygameHelper.constants import *
from PygameHelper.types import *
from functools import lru_cache

import pygame
from math import sin, cos, sqrt


# some of this functions are in classes for better organisation


_MISSING = object()


def lerp(start: Number, stop: Number, amount: Number) -> float:
    """
    Calculates a number between two numbers at a specific increment
    :param start: Number
    :param stop: Number
    :param amount: Number
    :return: float
    """
    if amount > 1 or amount < 0:
        if amount > 1:
            raise ValueError(f"amount in lerp function is bigger than 1")
        if amount < 0:
            raise ValueError(f"amount in lerp function is smaller than 0")
    return amount * (stop - start) + start


class _SO:  # shared object
    vertexes_list: List[List[Tuple[int, int]]] = []
    surfaces: List[Optional[pygame.surface.Surface]] = []
    loc_00: Vector = Vector()
    list_prev_00: List[Vector] = []


class Curves:
    @staticmethod
    def _quadratic(p1: CoordsType, p2: CoordsType, p3: CoordsType, t: Number) -> pygame.math.Vector2:
        return pygame.math.Vector2(
            lerp(lerp(p1[0], p2[0], t), lerp(p2[0], p3[0], t), t),
            lerp(lerp(p1[1], p2[1], t), lerp(p2[1], p3[1], t), t)
        )

    @classmethod
    def quadratic_bezier(
            cls,
            surface: pygame.surface.Surface,
            p1: CoordsType,
            p2: CoordsType,
            p3: CoordsType,
            delta: Number=0.03,
            color: ColorType=WHITE,
            width: Number=1
    ) -> pygame.Rect:
        """
        Quadratic bezier curve (1 static, 1 control and 1 static point)
        :param surface: pygame.surface.Surface
        :param p1: CoordsType
        :param p2: CoordsType
        :param p3: CoordsType
        :param delta: Union[int, float]
        :param color: ColorType
        :param width: Number
        :return: pygame.Rect
        """
        mul_am = int(1 / delta)
        return lines(
            surface,
            color,
            False,
            [cls._quadratic(p1, p2, p3, t / mul_am) for t in range(0, mul_am + 1, 1)],
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
            delta: Number=0.03,
            color: ColorType=WHITE,
            width: Number=1
    ) -> pygame.Rect:
        """
        it creates a bezier curve based on 4 points (1 static, 2 control points an 1 static) aka a cubic bezier
        :param surface: pygame.surface.Surface
        :param p1: CoordsType
        :param p2: CoordsType
        :param p3: CoordsType
        :param p4: CoordsType
        :param delta: Union[int, float]
        :param color: ColorType
        :param width: Number
        :return: pygame.Rect
        """
        if delta >= 1 or delta <= 0:
            if delta >= 1:
                raise ValueError(f"delta in bezier function is bigger or equal than 1")
            if delta <= 0:
                raise ValueError(f"delta in bezier function is smaller or equal than 0")
        mul_am = int(1 / delta)
        beginShape(surface)
        for t in range(0, mul_am + 1, 1):
            t /= mul_am
            v1 = cls._quadratic(p1, p2, p3, t)
            v2 = cls._quadratic(p2, p3, p4, t)
            vertex(lerp(v1.x, v2.x, t), lerp(v1.y, v2.y, t))
        return endShape(color=color, width=width)


class Draw:
    bezier = Curves.bezier
    quadratic_bezier = Curves.quadratic_bezier

    @staticmethod
    def push() -> None:
        """
        it saves the current 0, 0 location for drawing
        :return: None
        """
        _SO.list_prev_00.append(_SO.loc_00.copy())

    @staticmethod
    def translate(
        x: Union[Number, pygame.math.Vector2, Vector, Tuple[Number, Number], List[Number]],
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
        _SO.loc_00 = _SO.list_prev_00.pop().copy()

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
        x: Union[Number, pygame.math.Vector2, Vector, Tuple[Number, Number], List[Number]],
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
            outline: Optional[int]=None,
            outline_color: ColorType=BLACK
    ) -> pygame.Rect:
        """
        it ends the shape and draws the shape that was constructed by the beginShape and vertex
        :param closed: Optional[Union[int, bool]]=None
        :param fill: Optional[Union[int, bool]]=None
        :param color: ColorType=(255, 255, 255)
        :param width: int=1
        :param outline: Optional[int]=None
        :param outline_color: Optional[ColorType]
        :return: pygame.Rect
        """
        if not len(_SO.surfaces):
            raise ShapeError("shape was never started. start a shape with PygameHelper.beginShape")
        if fill:
            xx = sorted([v[0] for v in _SO.vertexes_list[~0]])
            yy = sorted([v[1] for v in _SO.vertexes_list[~0]])
            max_x = int(xx[~0])
            max_y = int(xx[~0])
            min_x = int(yy[0])
            min_y = int(yy[0])
            surf = pygame.surface.Surface((max_x, max_y))
            if color[0] == 255: surf.fill((color[0]-1, color[1], color[2])); surf.set_colorkey((color[0]-1, color[1], color[2]))
            if color[0] == 0: surf.fill((color[0]+1, color[1], color[2])); surf.set_colorkey((color[0]+1, color[1], color[2]))
            pygame.draw.polygon(surf, color, _SO.vertexes_list[~0])
            r = _SO.surfaces[~0].blit(surf, (min_x, min_y))
        else:
            r = lines(_SO.surfaces[~0], color, closed, _SO.vertexes_list[~0], width)
        if outline: lines(_SO.surfaces[~0], outline_color, closed, _SO.vertexes_list[~0], outline)
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


bezier = Curves.bezier
quadratic_bezier = Curves.quadratic_bezier

beginShape = Draw.beginShape
vertex = Draw.vertex
endShape = Draw.endShape

push = Draw.push
translate = Draw.translate
pop = Draw.pop

rect = Draw.rect
polygon = Draw.polygon
circle = Draw.circle
ellipse = Draw.ellipse
arc = Draw.arc
line = Draw.line
lines = Draw.lines
aaline = Draw.aaline
aalines = Draw.aalines

draw = Draw  # i like having classes capitalized but the draw to keep it similar to pygame


__all__ = [
    "draw",
    "bezier", "quadratic_bezier",
    "beginShape", "vertex", "endShape",
    "push", "translate", "pop",
    "rect", "polygon", "circle", "ellipse", "arc", "line", "lines", "aaline", "aalines"
]
