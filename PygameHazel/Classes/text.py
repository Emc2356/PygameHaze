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
texts that can be displayed
"""


from typing import Tuple, List

import pygame

from PygameHazel.constants import *
from PygameHazel.exceptions import *
from PygameHazel.utils import *


class SimpleText:
    """
    Creates a single-line text

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that buttons are going to be drawn in
    x: int
        the x position of the text
    y: int
        the y position of the text
    text: str
        the text of the text
    color: Tuple[int, int, int]
        the color of the text
    **kwargs: optional parameters
        optional parameters

    Methods:
    -----------
    update(centered_x=False, centered_x_pos: int=None):
        it updates the rect and the text
    draw():
        it draws the text
    """
    def __init__(self,
                 WIN: pygame.surface.Surface,
                 x: int,
                 y: int,
                 text: str,
                 color: Tuple[int, int, int]=BLACK,
                 **kwargs):
        self.WIN: pygame.surface.Surface = WIN
        self.x: int = int(x)
        self.y: int = int(y)
        self.color: Tuple[int, int, int] = color
        self.text: str = str(text)
        self.anchor: str = kwargs.get("anchor", TOPLEFT).lower()

        self.font_size: int = kwargs.get("font_size", 60)
        self.font_type: str = kwargs.get("font_type", "comicsans")
        self.antialias: bool = kwargs.get("antialias", True)
        self.font: pygame.font.Font = get_font(self.font_size, self.font_type)
        self.rendered_text: pygame.surface.Surface = None
        self.rendered_text_rect: pygame.Rect = None
        self.update()

        self.kwargs: dict = kwargs

    def update(self) -> None:
        """
        call this method to update the text otherwise the text on the screen wont change
        :return: None
        """
        self.rendered_text = self.font.render(self.text, self.antialias, self.color)
        self.rendered_text_rect = self.rendered_text.get_rect()
        try:
            self.rendered_text_rect.__setattr__(self.anchor, (self.x, self.y))
        except AttributeError:
            raise InvalidAnchor(f"""The anchor '{self.anchor}' is not a valid anchor.""")

    def draw(self) -> None:
        """
        it draws the text in the screen
        :return: None
        """
        self.WIN.blit(self.rendered_text, self.rendered_text_rect)

    def __repr__(self):
        return f"one line text at: [{self.x}, {self.y}] with text '{self.text}'"

    def __str__(self):
        return f"one line text at: [{self.x}, {self.y}] with text '{self.text}'"


class MultiLineText:
    """
    Creates a multi-line text

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that buttons are going to be drawn in
    x: int
        the x position of the text
    y: int
        the y position of the text
    text: str
        the text of the text
    color: Tuple[int, int, int]
        the color of the text
    **kwargs: optional parameters
        optional parameters

    Methods:
    -----------
    update(centered_x=False, centered_x_pos: int=None):
        it updates the rect and the text
    draw():
        it draws the text
    """
    def __init__(self,
                 WIN: pygame.surface.Surface,
                 x: int,
                 y: int,
                 text: str,
                 color: Tuple[int, int, int]=BLACK,
                 **kwargs):
        self.WIN: pygame.surface.Surface = WIN
        self.x: int = int(x)
        self.y: int = int(y)
        self.color: Tuple[int, int, int] = color
        self.text: str = str(text)

        self.font_size: int = kwargs.get("font_size", 60)
        self.font_type: str = kwargs.get("font_type", "comicsans")
        self.antialias: bool = kwargs.get("antialias", True)
        self.font: pygame.font.Font = get_font(self.font_size, self.font_type)
        self.rendered_texts: List[pygame.surface.Surface] = []
        self.update()

        self.kwargs: dict = kwargs
        
    def update(self, centered_x=False, centered_x_pos: int=None) -> None:
        """
        it sets-up the text. this method has to be called when the text changes
        :param centered_x: if the text is going to be x-centered
        :param centered_x_pos: the rect that is going to be used if centered_x is True
        :return: None
        """
        if centered_x and not centered_x_pos:
            raise MissingRequiredArgument(f"""in the "update method the centered_x_pos is missing.""")
        height = self.font.get_height()
        self.rendered_texts = []
        for i, text in enumerate(self.text.split("\n")):
            rendered_text_surface = self.font.render(text, self.antialias, self.color)

            if centered_x: pos = [centered_x_pos - rendered_text_surface.get_width()/2, self.y + (i * height)]
            else: pos = [self.x, self.y + (i * height)]
            self.rendered_texts.append([rendered_text_surface, pos])

    def draw(self) -> None:
        """
        it blits multiple lines on the screen
        :return: None
        """
        for surface, pos in self.rendered_texts:
            self.WIN.blit(surface, pos)

    def __repr__(self):
        return f"one line text at: [{self.x}, {self.y}] with text '{self.text}'"

    def __str__(self):
        return f"one line text at: [{self.x}, {self.y}] with text '{self.text}'"


__all__ = [
    "SimpleText",
    "MultiLineText"
]
