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
a quad tree implementation
"""

from typing import List, Any
from PygameHaze.types import *

import itertools
import pygame


class QuadTree:
    """
    QuadTree data structure

    Parameters:
    -----------
    space: pygame.Rect
        the location of the QuadTree
    capacity: int
        how many objects can it handle

    Methods:
    -----------
    get_items():
        it returns all of the objects of the QuadTree
    list_insert(objs: List[Any]):
        it inserts a list of objects in the QuadTree
    insert(obj: Any):
        it inserts a object on the QuadTree (it needs to have a .pos attribute)
    query(rectangle: pygame.Rect):
        it returns all of the objects that can be found in a given area
    """
    __slots__ = "space", "capacity", "storage", "children"

    def __init__(self, space: pygame.Rect, capacity: int) -> None:
        self.space: pygame.Rect = space
        self.capacity: int = capacity
        self.storage: List[Any] = []
        self.children: List[QuadTree] = []

    def get_items(self) -> List[Any]:
        """
        it returns all of the items that it has and everything from its children
        :return: List[Any]
        """
        return self.storage + list(itertools.chain.from_iterable((ch.get_items() for ch in self.children)))

    def subdivide(self) -> None:
        """
        it subdivides the quad tree
        :return: None
        """
        new_size = self.space.w/2, self.space.h/2
        self.children.append(QuadTree(pygame.Rect(*self.space.topleft, *new_size), self.capacity))
        self.children.append(QuadTree(pygame.Rect(*self.space.midtop, *new_size), self.capacity))
        self.children.append(QuadTree(pygame.Rect(*self.space.center, *new_size), self.capacity))
        self.children.append(QuadTree(pygame.Rect(*self.space.midleft, *new_size), self.capacity))

    def list_insert(self, objs: List[Any]) -> "QuadTree":
        """
        it inserts a list inside the quad tree
        :param objs: List[Any]
        :return: QuadTree (the instance)
        """
        [self.insert(obj) for obj in objs]
        return self

    def insert(self, obj: Any) -> bool:
        """
        it accepts an object and inserts it into the quad tree (the object needs to have a .pos attribute)
        :param obj: Any
        :return: bool
        """
        if not self.space.collidepoint(obj.pos):
            return False
        if len(self.storage) < self.capacity:
            self.storage.append(obj)
            return True
        else:
            if not self.children:
                self.subdivide()
            for ch in self.children:
                if ch.insert(obj):
                    return True
        return False

    def query(self, rectangle: pygame.Rect) -> List[Any]:
        """
        it accepts an area to look for items
        :param rectangle: pygame.Rect
        :return: List[Any]
        """
        if rectangle.contains(self.space):
            return self.get_items()
        found = []
        if self.space.colliderect(rectangle):
            for obj in self.storage:
                if rectangle.collidepoint(obj.pos):
                    found.append(obj)
            for ch in self.children:
                found.extend(ch.query(rectangle))
        return found

    def draw(self, WIN: pygame.surface.Surface, color: ColorType=(255, 255, 255)) -> None:
        """
        it draws the quad tree (wireframe)
        :param WIN: pygame.surface.Surface
        :param color: Tuple[int, int, int]
        :return: None
        """
        pygame.draw.rect(WIN, color, self.space, 1)
        for ch in self.children:
            ch.draw(WIN, color)
