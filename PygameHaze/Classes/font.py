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
a custom font that can be generated
throw a given image
"""


from typing import Tuple, List, Dict, Union
from functools import cached_property, lru_cache
from PygameHaze.types import *

import pygame

from PygameHaze.Classes import SpriteSheet
from PygameHaze.utils import *
from PygameHaze.exceptions import *


class Font:
    """
    a custom Font object that can be used with fonts from surfaces

    Parameters:
    -----------
    type: str
        the path to the font image
    size: float
        the size multiplier for the font
    barrier: Tuple[int, int, int]
        the color of the barrier between the letters
    colorkey_for_char: Tuple[int, int, int] or int
        the colorkey for the spritesheet
    spacing: int=1
        how much spacing per letter 1 is enough

    Methods:
    -----------
    get_size():
        it returns a tuple with the max width and height of the characters
    get_width():
        it returns the max width of the characters
    get_height():
        it returns the max height of the characters
    render(text: str, max_width: float=inf):
        it returns a surface with a text blited on it
    render_to(surface: pygame.surface.Surface, x: float, y: float, text: str, max_width: float=float("inf")):
        it renders the text directly into a given surface
    """
    def __init__(self, type: str, size: float=1, barrier: Tuple[int, int, int]=(0, 0, 0),
                 colorkey_for_char: Union[Tuple[int, int, int], int]=None, spacing: int=1) -> None:
        self._type: str = type
        self._barrier: Tuple[int, int, int] = barrier
        self._spacing: int = int(spacing * size)
        self._spritesheet: SpriteSheet = SpriteSheet(type, colorkey_for_char)
        self._order: List[str] = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
            "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            ".", "-", "+", "/", "*", "=", ",", "[", "]", "(", ")", "{", "}",
            "'", "!", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "_", "|", "\\", "<", ">"
        ]
        self._rendered_chars: Dict[str, pygame.surface.Surface] = {}

        cur_index = 0
        sheet = self._spritesheet.sheet
        char_width = 0
        for x in range(sheet.get_width()):
            color = sheet.get_at((x, 0))[0:3]
            if color == self._barrier:
                self._rendered_chars[self._order[cur_index]] = resizex(self._spritesheet.clip((x-char_width, 0, char_width, sheet.get_height())).copy(), size)
                char_width = 0
                cur_index += 1
            else: char_width += 1

        self._max_h: int = max([surf.get_height() for surf in self._rendered_chars.values()])
        self._max_w: int = max([surf.get_width() for surf in self._rendered_chars.values()])

    def get_size(self) -> Tuple[int, int]:
        """
        it returns a tuple with the max width and height of the characters
        :return: Tuple[int, int]
        """
        return self._max_w, self._max_h

    def get_width(self) -> int:
        """
        it returns the max width of the characters
        :return: int
        """
        return self._max_w

    def get_height(self) -> int:
        """
        it returns the max height of the characters
        :return: int
        """
        return self._max_h

    @cached_property
    def size(self) -> Tuple[int, int]:
        return self._max_w, self._max_h

    @cached_property
    def w(self) -> int:
        return self._max_w

    @cached_property
    def h(self) -> int:
        return self._max_h

    @lru_cache
    def __word_width_render(self, text: str) -> int:
        return sum([self._rendered_chars[char].get_width() + self._spacing for char in text.split("\n")[0]])

    @lru_cache
    def render(self, text: str, max_width: float=float("inf")) -> pygame.surface.Surface:
        """
        it returns a surface with a text blited on it
        :param text: str
        :param max_width: float=infinite
        :return: pygame.surface.Surface
        """
        storage = []
        width = tempW = 0
        height = self._max_h
        for word in text.split(" "):
            if self.__word_width_render(word) + tempW > max_width:
                if self.__word_width_render(word) > max_width:
                    raise WordTooLong(f"the string: '{word}' is {self.__word_width_render(word) - max_width}pxls")
                height += self._max_h + self._spacing
                width = max(tempW, width)
                tempW = 0

            for char in word:
                if char != "\n":
                    if char not in self._rendered_chars:
                        raise UnrecognisedCharacter(f"character '{char}' was not recognized")
                    storage.append([self._rendered_chars[char], pygame.Rect(tempW, height - self._max_h, 0, 0)])
                    tempW += self._rendered_chars[char].get_width() + self._spacing
                    continue
                height += self._max_h + self._spacing
                width = tempW if tempW > width else width
                tempW = 0

            tempW += self._max_w * int("\n" not in word)

        surface = pygame.surface.Surface((max(width, tempW) - self._max_w, height))
        surface.set_colorkey(surface.get_at((0, 0)))

        surface.blits(storage, False)

        return surface

    def render_to(self, surface: pygame.surface.Surface, pos: CoordsType,
                  text: str, max_width: float=float("inf")) -> pygame.Rect:
        """
        it renders a given text directly in a surface
        :param surface: pygame.surface.Surface
        :param pos: AnyCoordsType
        :param text: str
        :param max_width: float=infinite
        :return: pygame.Rect
        """
        return surface.blit(self.render(text, max_width), pos)
