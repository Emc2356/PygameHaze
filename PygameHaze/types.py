"""
this are some types taken from inside the pygame library about some common types or commonly needed types
"""

from typing import Union, List, Tuple, Iterable, Iterator, Generator, Any
from pathlib import Path
import pygame
import os

CoordsType = Union[
    Tuple[float, float], List[float],
    pygame.math.Vector2, Iterable[float], Iterator[float], Generator[float, Any, Any]
]
ColorType = Union[pygame.Color, str, Tuple[float, float, float], List[float], int, Tuple[float, float, float, float]]
RectType = Union[
    pygame.Rect,
    Tuple[float, float, float, float],
    Tuple[Tuple[float, float], Tuple[float, float]],
    List[pygame.math.Vector2],
    Tuple[pygame.math.Vector2, pygame.math.Vector2],
    Iterable[pygame.math.Vector2],
    List[float]
]
PathType = Union[str, bytes, os.PathLike[str], os.PathLike[bytes], Path]
types = [CoordsType, RectType, ColorType, PathType]

__all__ = ["CoordsType", "ColorType", "RectType", "types", "PathType"]
