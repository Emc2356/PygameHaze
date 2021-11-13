"""
this are some types taken from inside the pygame library about some common types or commonly needed types
"""

from typing import Union, List, Tuple, Iterable
import PygameHelper.Classes.vector as vector
import pygame


Number = Union[int, float]
VectorType = Union[vector.Vector, pygame.math.Vector2]
CoordsType = Union[Tuple[Number, Number], List[Number], VectorType]
ColorType = Union[pygame.Color, str, Tuple[Number, Number, Number], List[Number], int, Tuple[Number, Number, Number, Number]]
RectType = Union[
    pygame.Rect, Tuple[Number, Number, Number, Number], Tuple[Tuple[Number, Number], Tuple[Number, Number]],
    List[pygame.math.Vector2], Tuple[pygame.math.Vector2, pygame.math.Vector2], Iterable[pygame.math.Vector2],
    List[Union[vector.Vector]], Tuple[Union[vector.Vector], Union[vector.Vector]], Iterable[Union[vector.Vector]], List[Number]
]

types = [Number, VectorType, CoordsType, RectType, ColorType]

__all__ = ["Number", "VectorType", "CoordsType", "ColorType", "RectType", "types"]
