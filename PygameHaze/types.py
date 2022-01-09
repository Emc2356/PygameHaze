"""
this are some types taken from inside the pygame library about some common types or commonly needed types
"""

from typing import Union, List, Tuple, Iterable
import pygame
import os


Number = Union[int, float]
CoordsType = Union[Tuple[Number, Number], List[Number]]
ColorType = Union[pygame.Color, str, Tuple[Number, Number, Number], List[Number], int, Tuple[Number, Number, Number, Number]]
RectType = Union[
    pygame.Rect,
    Tuple[Number, Number, Number, Number],
    Tuple[Tuple[Number, Number], Tuple[Number, Number]],
    List[pygame.math.Vector2],
    Tuple[pygame.math.Vector2, pygame.math.Vector2],
    Iterable[pygame.math.Vector2],
    List[Number]
]
PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes]]
types = [Number, CoordsType, RectType, ColorType, PathType]

__all__ = ["Number", "CoordsType", "ColorType", "RectType", "types", "PathType"]
