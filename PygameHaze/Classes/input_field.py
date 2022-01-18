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
input fields
"""


from typing import Tuple

import pygame

from PygameHaze.utils import *
from PygameHaze.constants import *
from PygameHaze.exceptions import *


class InputField:
    """
    Creates a input field on the screen

    Parameters:
    -----------
    x: int
        the x position of the button
    y: int
        the y position of the button
    w: int
        the width of the button
    h: int
        the height of the button
    base_color: Tuple[int, int, int]
        the color of the field
    text_color: Tuple[int, int, int]
        the color of the text
    **kwargs: optional parameters
        optional parameters

    Methods:
    -----------
    update():
        it updates the text and the rect
    draw(pygame.surface.Surface):
        it draws the input field
    get_width():
        it returns the width of the field
    get_height():
        it returns the height of the field
    write(str):
        it writes a character in the input field
    clear():
        it clears the text in the input field
    delete_last():
        it deletes the last character from the input field
    get_text():
        it returns the text of the input field
    is_empty():
        it tells you whether the field is emtpy or not
    event_handler(pygame.event.Event):
        it checks the events and this is how you write in hte field
    """
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 base_color: Tuple[int, int, int]=WHITE,
                 text_color: Tuple[int, int, int]=BLACK,
                 **kwargs):
        # cords stuff
        self.x: int = x
        self.y: int = y
        self.h: int = h
        self.w: int = w
        self.anchor: str = kwargs.get("anchor", TOPLEFT)

        # color stuff
        self.base_color: Tuple[int, int, int] = base_color
        self.inactive_color: Tuple[int, int, int] = kwargs.get("inactive_color", (255, 0, 0))
        self.active_color: Tuple[int, int, int] = kwargs.get("active_color", (0, 255, 0))
        self.outline: int = kwargs.get("outline", 2)

        # font stuff
        self.font_size: int = kwargs.get("font_size", 60)
        self.font_type: str = kwargs.get("font_type", "comicsans")
        self.text_color: Tuple[int, int, int] = text_color
        self.font: pygame.font.Font = get_font(self.font_size, self.font_type)
        self.text: str = ""
        self.antialias: bool = kwargs.get("antialias", True)
        self.focused: bool = False

        self.MAX: int = kwargs.get("MAX", 0)
        self.delete_mode: bool = False

        self.base_rect: pygame.Rect = None
        self.rendered_text: pygame.surface.Surface = None
        self.rendered_text_rect: pygame.Rect = None

        self.update()

    def update(self) -> None:
        """
        it sets up the field with the text if you don't call this method what is displayed on the screen wont be changing
        :return: None
        """
        try:
            self.base_rect = pygame.Rect(self.x, self.y, self.w, self.h)
            self.base_rect.__setattr__(self.anchor, (self.x, self.y))
        except AttributeError:
            raise InvalidAnchor(f"""The anchor '{self.anchor}' is not a valid anchor.""")

        self.rendered_text = self.font.render(str(self.text), self.antialias, self.text_color)
        self.rendered_text_rect = self.rendered_text.get_rect()
        self.rendered_text_rect.center = self.base_rect.center

    def draw(self, surface: pygame.surface.Surface) -> None:
        """
        draws the bar in the window
        :param surface: the surface that the field will be drawn
        :type surface: pygame.surface.Surface
        :return: None
        """
        pygame.draw.rect(surface, self.active_color if self.focused else self.inactive_color, self.base_rect)
        pygame.draw.rect(
            surface, self.base_color, pygame.Rect(
                self.base_rect[0] + self.outline, self.base_rect[1] + self.outline, self.base_rect[2] - self.outline*2, self.base_rect[3] - self.outline*2
            )
        )
        surface.blit(self.rendered_text, self.rendered_text_rect)

    def get_width(self) -> int:
        """
        returns the width of the bar
        :return: int
        """
        return self.w

    def get_height(self) -> int:
        """
        returns the height of the bar
        :return: int
        """
        return self.h

    def write(self, character: str) -> None:
        """
        writes a character to the field you don't need to call the update() method as it is automatically called when the character is written
        :param character: str
        :return: None
        """
        if self.MAX > 0:
            if len(self.text) >= self.MAX:
                return
            self.text += character
            self.update()
            return
        self.text += character
        self.update()
        return

    def clear(self) -> None:
        """
        clears the text that is writen you don't need to call the update() method as it is automatically called when the character is written
        :return: None
        """
        self.text = ""
        self.update()

    def delete_last(self) -> None:
        """
        deletes the last character of the text
        :return: None
        """
        self.text = self.text[:-1]
        self.update()

    def get_text(self) -> str:
        """
        it gives the current text of the field
        :return: self.text: str
        """
        return self.text

    def is_empty(self) -> bool:
        """
        tells if the field is empty
        :return: bool
        """
        return self.text == ""

    def event_handler(self, event: pygame.event.Event) -> None:
        """
        used only with numbers
        :param event: pygame.event.Event
        :return: None
        """
        if left_click(event):
            if self.base_rect.collidepoint(event.pos):
                self.focused = True
            else:
                self.focused = False
        if self.focused:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.delete_mode = True
                else:
                    self.write(event.unicode)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.delete_mode = False

        if self.delete_mode:
            self.delete_last()


class InputFieldNumbers(InputField):
    """
    Creates a input field on the screen

    Parameters:
    -----------
    x: int
        the x position of the button
    y: int
        the y position of the button
    w: int
        the width of the button
    h: int
        the height of the button
    base_color: Tuple[int, int, int]
        the color of the field
    text_color: Tuple[int, int, int]
        the color of the text
    **kwargs: optional parameters
        optional parameters

    Methods:
    -----------
    update():
        it updates the text and the rect
    draw(pygame.surface.Surface):
        it draws the input field
    get_width():
        it returns the width of the field
    get_height():
        it returns the height of the field
    write(str):
        it writes a character in the input field
    clear():
        it clears the text in the input field
    delete_last():
        it deletes the last character from the input field
    get_text():
        it returns the text of the input field
    is_empty():
        it tells you whether the field is emtpy or not
    event_handler(pygame.event.Event):
        it checks the events and this is how you write in hte field
    """
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 base_color: Tuple[int, int, int]=WHITE,
                 text_color: Tuple[int, int, int]=BLACK,
                 **kwargs):
        super().__init__(x, y, w, h, base_color, text_color, **kwargs)

    def event_handler(self, event) -> None:
        """
        used only with numbers
        :param event: pygame.Event
        :return: None
        """
        if left_click(event):
            if self.base_rect.collidepoint(event.pos):
                self.focused = True
            else:
                self.focused = False
        if self.focused:
            if event.type == pygame.KEYDOWN:
                if event.unicode.isdigit():
                    self.write(event.unicode)
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.delete_mode = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.delete_mode = False

        if self.delete_mode:
            self.delete_last()


class InputFieldLetters(InputField):
    """
    Creates a input field on the screen

    Parameters:
    -----------
    x: int
        the x position of the button
    y: int
        the y position of the button
    w: int
        the width of the button
    h: int
        the height of the button
    base_color: Tuple[int, int, int]
        the color of the field
    text_color: Tuple[int, int, int]
        the color of the text
    **kwargs: optional parameters
        optional parameters

    Methods:
    -----------
    update():
        it updates the text and the rect
    draw(pygame.surface.Surface):
        it draws the input field
    get_width():
        it returns the width of the field
    get_height():
        it returns the height of the field
    write(str):
        it writes a character in the input field
    clear():
        it clears the text in the input field
    delete_last():
        it deletes the last character from the input field
    get_text():
        it returns the text of the input field
    is_empty():
        it tells you whether the field is emtpy or not
    event_handler(pygame.event.Event):
        it checks the events and this is how you write in hte field
    """
    def __init__(self,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 base_color: Tuple[int, int, int]=WHITE,
                 text_color: Tuple[int, int, int]=BLACK,
                 **kwargs):
        super().__init__(x, y, w, h, base_color, text_color, **kwargs)

    def event_handler(self, event: pygame.event.Event) -> None:
        """
        used only with numbers
        :param event: pygame.Event
        :return: None
        """
        if left_click(event):
            if self.base_rect.collidepoint(event.pos):
                self.focused = True
            else:
                self.focused = False
        if self.focused:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    self.delete_mode = True
                elif str(event.unicode).startswith("\t") or str(event.unicode).startswith("\r"):
                    pass
                elif event.unicode != "" and not str(event.unicode).startswith("\t") or not str(event.unicode).startswith("\r"):
                    self.write(event.unicode)
            elif event.type == pygame.KEYUP:
                self.delete_mode = False

        if self.delete_mode:
            self.delete_last()
