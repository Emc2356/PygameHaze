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
some useful functions for pygame
and general use
"""

from typing import (
    List,
    Tuple,
    Iterable,
    Generator,
    Union,
    Iterator,
    Sequence,
    TypeVar,
    Any,
    Optional,
)
from functools import lru_cache

import pygame
import json

from PygameHaze.constants import *
from PygameHaze.types import *

NeighborOutputType = TypeVar("NeighborOutputType")


def left_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has left-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1


def middle_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has middle-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 2


def right_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has right-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 3


@lru_cache()
def get_font(size: int, type_of_font: Optional[str] = None) -> pygame.font.Font:
    """
    it returns a font object with the given sie and type of font
    :param size: the size of the font
    :param type_of_font: the type of the font, it can be a path or a sys font
    :type size: int
    :type type_of_font: str
    :return: pygame.font.Font
    """
    if type_of_font is None or type_of_font.endswith(".ttf"):
        return pygame.font.Font(type_of_font, size)
    return pygame.font.SysFont(type_of_font, size)


@lru_cache()
def wrap_multi_lines(
    text: str,
    font: pygame.font.Font,
    max_width: int,
    max_height: int = 0,
    antialias: bool = True,
) -> List[str]:
    """
    it returns a list of strings
    :param text: str
    :param font: pygame.font.Font
    :param max_width: int
    :param max_height: int=0
    :param antialias: bool=True
    :return: List[str]
    """
    finished_lines = [""]
    render = font.render

    for word in text.split(" "):
        w = render(word, antialias, BLACK).get_width()
        # check if one word is too long to fit in one line
        if w > max_width:
            raise ValueError(
                f"word '{word}' is too long to fit in the given width by {w - max_width}pxls"
            )

        if (
            render(f"{finished_lines[~0]} {word}", antialias, BLACK).get_width()
            > max_width
            or "\n" in word
        ):
            finished_lines.append(f"{word}")
        else:
            finished_lines[~0] += f" {word}"
    finished_lines[0] = finished_lines[0][1:]
    if max_height > 0:
        h = 0
        for line in finished_lines:
            h += render(line, antialias, BLACK).get_height()

        if h > max_height:
            raise ValueError(
                f"height limit exceeded {max_height} by {h - max_height}pxls"
            )

    return finished_lines


def blit_list(
    surface: pygame.surface.Surface,
    pos: CoordsType,
    lines: List[str],
    font: pygame.font.Font,
    center_x_pos: int = None,
    color: ColorType = BLACK,
    doreturn: bool = True,
) -> Optional[pygame.Rect]:
    """
    it blits in a surface a list of strings
    :param surface: the target surface
    :param pos: the x, y position for the drawing
    :param lines: a list of strings that will be drawn
    :param font: the font object that will be used for the rendering
    :param center_x_pos: if this is passed then the text will be centered in the x axis
    :param color: the color of the font
    :param doreturn: whether the function is going to return the rect
    :type surface: pygame.surface.Surface
    :type pos: Sequence[int]
    :type lines: List[str]
    :type font: pygame.font.Font
    :type center_x_pos: Optional[int]
    :type color: ColorType
    :type doreturn: bool
    :return: Optional[pygame.rect.Rect]
    """
    if center_x_pos and not center_x_pos:
        raise ValueError("Missing 'centered_x_pos'")
    x, y, *_ = pos
    height = font.get_height()
    blit_seq = (
        [
            (
                rendered_text_surface,
                (
                    center_x_pos - rendered_text_surface.get_width() / 2,
                    y + (i * height),
                ),
            )
            for i, rendered_text_surface in enumerate(
                map(lambda text: font.render(text, True, color), lines)
            )
        ]
        if center_x_pos
        else [
            (rendered_text_surface, (x, y + (i * height)))
            for i, rendered_text_surface in enumerate(
                map(lambda text: font.render(text, True, color), lines)
            )
        ]
    )
    return surface.blits(blit_seq, doreturn)


def flatten(iterable: Union[Sequence, Iterable, Iterator, Generator, map]) -> Generator:
    """
    it takes a iterable object and it flattens the object
    :param iterable: Iterable Sequence
    :return: Generator
    """
    for item in iterable:
        if isinstance(item, list) or isinstance(item, tuple):
            for subitem in flatten(item):
                yield subitem
        else:
            yield item


def read_json(path: PathType) -> dict:
    """
    it returns the cloth data from a file
    :param path: str
    :return: Dict
    """
    with open(path, "r") as f:
        return json.loads(f.read())


def get_neighbors(
    grid: List[List[NeighborOutputType]],
    target: Union[Tuple[int, int], List[int], Sequence[int]],
    diagonal: bool = False,
) -> Generator[NeighborOutputType, None, None]:
    """
    it returns the neighbors of a cell
    :param grid: the grid that the neighbors will be taken out of
    :param target: Union[Tuple[int, int], List[int, int], Sequence[int]]
    :param diagonal: whether it will check for diagonal neighbors (default=False)
    :type grid: List[List[Any]]
    :type target: Union[Tuple[int, int], List[int, int], Sequence[int]]
    :type diagonal: bool
    :return: List[Any]
    """
    columns = len(grid)
    rows = len(grid[0])
    oi, oj, *_ = target

    indexes = [(oi - 1, oj), (oi, oj - 1), (oi, oj + 1), (oi + 1, oj)] + [
        (oi - 1, oj - 1),
        (oi - 1, oj + 1),
        (oi + 1, oj + 1),
        (oi + 1, oj - 1),
    ] * bool(diagonal)

    for i, j in indexes:
        if not (i == oi and j == oj) and 0 <= i < columns and 0 <= j < rows:
            yield grid[i][j]


def get_neighbors_index(
    grid: List[List[Any]],
    target: Union[Tuple[int, int], List[int], Sequence[int]],
    diagonal: bool = False,
) -> Generator:
    """
    it returns the directly adjacent cells index (it makes the assumption that it has rows of the same length)
    :param grid: List[List[Any]]
    :param target: Union[Tuple[int, int], List[int, int], Sequence[int]]
    :param diagonal:
    :return: List[Any]
    """
    columns = len(grid) - 1
    rows = len(grid[0]) - 1
    oi, oj = target

    indexes = [(oi - 1, oj), (oi, oj - 1), (oi, oj + 1), (oi + 1, oj)] + [
        (oi - 1, oj - 1),
        (oi - 1, oj + 1),
        (oi + 1, oj + 1),
        (oi + 1, oj - 1),
    ] * bool(diagonal)

    for i, j in indexes:
        if not (i == oi and j == oj) and 0 <= i <= columns and 0 <= j <= rows:
            yield i, j


def combine_rects(rects: List[RectType]) -> pygame.Rect:
    """
    it creates the smallest possible rect that contains all of the rects
    :param rects: List[RectType]
    :return: RectType
    """
    x = sorted(pygame.Rect(r).x for r in rects)
    y = sorted(pygame.Rect(r).y for r in rects)
    return pygame.Rect(x[0], y[0], x[~0] - x[0], y[~0] - y[0])


__all__ = [
    "left_click",
    "middle_click",
    "right_click",
    "get_font",
    "wrap_multi_lines",
    "blit_list",
    "flatten",
    "read_json",
    "get_neighbors",
    "get_neighbors_index",
    "combine_rects",
]
