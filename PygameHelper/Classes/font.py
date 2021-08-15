"""
MIT License

Copyright (c) 2021 Emc2356

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from typing import Tuple, List, Dict

import pygame

from PygameHelper.Classes import SpriteSheet
from PygameHelper.utils import *
from PygameHelper.constants import *
from PygameHelper.exceptions import *


class Font:
    """
    Creates a button on the screen

    Parameters:
    -----------
    type: str
        the path to the font image
    size: int or float
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
    render(str, max_width=inf):
        it returns a surface with a text blited on it
    """
    def __init__(self, type: str, size: int or float=1, barrier: Tuple[int, int, int]=(0, 0, 0),
                 colorkey_for_char: Tuple[int, int, int] or int=None, spacing: int=1) -> None:
        self.type: str = type
        self.barrier: Tuple[int, int, int] = barrier
        self.spacing: int = spacing * size
        self.spritesheet: SpriteSheet = SpriteSheet(type, colorkey_for_char)
        self.order: List[str] = [
            "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            ".", "-", "+", "/", "*", "=", ",", "[", "]", "(", ")", "{", "}", "'", "!", "?", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "_", "|", "\\", "<", ">"
        ]
        self.rendered_chars: Dict[str, pygame.surface.Surface] = {}

        cur_index = 0
        sheet = self.spritesheet.get_sheet()
        char_width = 0
        for x in range(sheet.get_width()):
            color = sheet.get_at((x, 0))[0:3]
            if color == self.barrier:
                self.rendered_chars[self.order[cur_index]] = resizex(self.spritesheet.clip((x-char_width, 0, char_width, sheet.get_height())).copy(), size)
                char_width = 0
                cur_index += 1
            else: char_width += 1

        self.max_h: int = max([surf.get_height() for surf in self.rendered_chars.values()])
        self.min_h: int = min([surf.get_height() for surf in self.rendered_chars.values()])
        self.max_w: int = max([surf.get_width() for surf in self.rendered_chars.values()])
        self.min_w: int = min([surf.get_width() for surf in self.rendered_chars.values()])

    def get_size(self) -> Tuple[int, int]:
        """
        it returns a tuple with the max width and height of the characters
        :return: Tuple[int, int]
        """
        return self.max_w, self.max_h

    def get_width(self) -> int:
        """
        it returns the max width of the characters
        :return: int
        """
        return self.max_w

    def get_height(self) -> int:
        """
        it returns the max height of the characters
        :return: int
        """
        return self.max_h

    def __word_width_render(self, text: str) -> int:
        return sum([self.rendered_chars[char].get_width() + self.spacing for char in text.split("\n")[0]])

    def render(self, text: str, max_width: int or float=float("inf")) -> pygame.surface.Surface:
        """
        it returns a surface with a text blited on it
        :param text: str
        :param max_width: int or float=inf
        :return: pygame.surface.Surface
        """
        storage: List[List[pygame.surface.Surface, List[int, int]]] = []
        string_c = text.split(LINE_SPLITTER)
        words = []
        for s in string_c: words += s.split(" ")
        width, temp_w, height = 0, 0, self.max_h
        for word in words:
            word_length = self.__word_width_render(word)
            if word_length + temp_w > max_width:
                if word_length > max_width:
                    raise WordTooLong(f"the string: '{word}' is {word_length - max_width}pxls")
                height += self.max_h + self.spacing
                width = temp_w if temp_w > width else width
                temp_w = 0

            for ltr in word:
                if ltr != "\n":
                    storage.append([self.rendered_chars[ltr], [temp_w, height - self.max_h]])
                    temp_w += self.rendered_chars[ltr].get_width() + self.spacing
                else:
                    height += self.max_h + self.spacing
                    width = temp_w if temp_w > width else width
                    temp_w = 0

            temp_w += self.max_w

        width = (temp_w if temp_w > width else width) - self.max_w

        surface = pygame.surface.Surface((width, height))
        surface.set_colorkey(surface.get_at((0, 0)))

        for surf, pos in storage:
            surface.blit(surf, pos)

        return surface
