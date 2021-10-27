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
a class for handling spritesheets
"""


from typing import Tuple, List

import pygame

from PygameHelper.utils import *


class SpriteSheet:
    """
    Creates a button on the screen

    Parameters:
    -----------
    path: str
        the path for the image that is going to be used for the spritesheet
    colorkey: Tuple[int, int, int] or int
        what pixel is going to be transparent -1 is using the pixel at (0, 0)

    Methods:
    -----------
    get_sheet():
        it returns the sheet that is stored
    clip([x, y, w, h], colorkey):
        it returns a image in the specified coordinates
    """
    def __init__(self, path: str, colorkey: Tuple[int, int, int] or int=None):
        self.sheet: pygame.surface.Surface = load_image(path)

        if colorkey is not None:
            if colorkey == -1:
                self.sheet.set_colorkey(self.sheet.get_at((0, 0)))
            else:
                self.sheet.set_colorkey(colorkey)

    def get_sheet(self) -> pygame.surface.Surface:
        return self.sheet

    def clip(self, r: Tuple[int, int, int, int], colorkey: Tuple[int, int, int] or int=None) -> pygame.surface.Surface:
        """
        Load a specific image from a specific rectangle.
        :param r: Tuple[int, int, int, int]
        :param colorkey: Tuple[int, int, int]
        :return: pygame.surface.Surface
        """
        rect = pygame.Rect(r)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def clips(self, rects: List[Tuple[int, int, int, int]], colorkey: Tuple[int, int, int] or int=None) -> List[pygame.surface.Surface]:
        """
        it returns a list with images
        :param rects: List[Tuple[int, int, int, int]]
        :param colorkey: Tuple[int, int, int] or int
        :return: List[pygame.surface.Surface
        """
        return [self.clip(r, colorkey) for r in rects]
