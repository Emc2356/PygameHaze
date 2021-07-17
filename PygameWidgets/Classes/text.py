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


from typing import Tuple

import pygame

from PygameWidgets.constants import *
from PygameWidgets.exceptions import *


class SimpleText:
    def __init__(self,
                 WIN: pygame.surface.Surface,
                 x: int,
                 y: int,
                 text: str,
                 color: Tuple[int, int, int]=BLACK,
                 **kwargs):
        self.WIN = WIN
        self.x = int(x)
        self.y = int(y)
        self.color = color
        self.text = str(text)
        self.anchor = kwargs.get("anchor", TOPLEFT)

        self.font_size = kwargs.get("font_size", 60)
        self.font_type = kwargs.get("font_type", "comicsans")
        self.antialias = kwargs.get("antialias", True)
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.rendered_text = None
        self.rendered_text_rect = None
        self.update_text(self.x, self.y)

        self.kwargs = kwargs

    def update_text(self, x, y):
        """
        call this method to update the text otherwise the text on the screen wont change
        :return: None
        """
        self.rendered_text = self.font.render(self.text, self.antialias, self.color)
        self.rendered_text_rect = self.rendered_text.get_rect()
        try:
            self.rendered_text_rect.__setattr__(self.anchor, (x, y))
        except AttributeError:
            raise InvalidAnchor(f"""The anchor '{self.anchor}' is not a valid anchor.""")

        self.x = x
        self.y = y

    def draw(self):
        """
        it draws the text in the screen
        :return: None
        """
        self.WIN.blit(self.rendered_text, self.rendered_text_rect)


class MultiText:
    def __init__(self,
                 WIN: pygame.surface.Surface,
                 x: int,
                 y: int,
                 text: str,
                 color: Tuple[int, int, int]=BLACK,
                 **kwargs):
        self.WIN = WIN
        self.x = x
        self.y = y
        self.text = text
        self.color = color

        self.font_size = kwargs.get("font_size", 60)
        self.font_type = kwargs.get("font_type", "comicsans")
        self.antialias = kwargs.get("antialias", True)
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.rendered_texts = []
        self.rendered_text_rects = []

    def _blit_multiple_lines(self, x, y, centered_x=True, centered_rect: pygame.rect.Rect=None):
        """
        it blits multiple lines on the screen
        :param x: the x position of the text
        :param y: the y position of the text
        :param centered_x: if the text is going to be x-centered
        :param centered_rect: the rect that is going to be used if centered_x is True
        :return: None
        """
        if not centered_rect:
            raise MissingRequiredArgument(f"""in the "_blit_multiple_lines method the centered_rect is missing.""")
        height = self.font.get_height()
        lines = self.text.split(LINE_SPLITTER)
        for i, text in enumerate(lines):
            rendered_text_surface = self.font.render(text, self.antialias, self.color)

            if centered_x:
                self.WIN.blit(rendered_text_surface, (centered_rect.centerx - rendered_text_surface.get_width()/2, y + (i * height)))

            else:
                self.WIN.blit(rendered_text_surface, (x, y + (i * height)))