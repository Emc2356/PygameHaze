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

from PygameWidgets.functions import *
from PygameWidgets.constants import *
from PygameWidgets.exceptions import *


class InputField:
    def __init__(self,
                 WIN: pygame.Surface,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 base_color: tuple[int, int, int]=(255, 255, 255),
                 text_color: tuple[int, int, int]=BLACK,
                 **kwargs):
        # set the win
        self.WIN = WIN

        # cords stuff
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.anchor = kwargs.get("anchor", TOPLEFT)

        # color stuff
        self.base_color = base_color
        self.inactive_color = kwargs.get("inactive_color", (255, 0, 0))
        self.active_color = kwargs.get("active_color", (0, 255, 0))
        self.outline = kwargs.get("outline", 2)

        # font stuff
        self.font_size = kwargs.get("font_size", 60)
        self.font_type = kwargs.get("font_type", "comicsans")
        self.text_color = text_color
        self.font = get_font(self.font_size, self.font_type)
        self.text = ""
        self.antialias = kwargs.get("antialias", True)
        self.focused = False

        self.MAX = kwargs.get("MAX", 0)

        self.base_rect = None
        self.rendered_text = None
        self.rendered_text_rect = None

        self.update_field()

    def update_field(self):
        """
        it sets up the field with the text if you dont call this method what is displayed on the screen wont be changing
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

    def draw(self):
        """
        draws the bar in the window
        :return: None
        """
        pygame.draw.rect(self.WIN, self.active_color if self.focused else self.inactive_color, self.base_rect)
        pygame.draw.rect(self.WIN, self.base_color, pygame.Rect(
            self.base_rect[0] + self.outline, self.base_rect[1] + self.outline, self.base_rect[2] - self.outline*2, self.base_rect[3] - self.outline*2
        ))
        self.WIN.blit(self.rendered_text, self.rendered_text_rect)

    def get_width(self):
        """
        returns the width of the bar
        :return: int
        """
        return self.w

    def get_height(self):
        """
        returns the height of the bar
        :return: int
        """
        return self.h

    def write(self, character):
        """
        writes a character to the field
        :param character: any
        :param MAX: int
        :return: None
        """
        if self.MAX > 0:
            if len(self.text) >= self.MAX:
                return
            self.text += character
            self.update_field()
            return
        self.text += character
        self.update_field()
        return

    def clear(self):
        """
        clears the tect that is writen
        :return: None
        """
        self.text = ""

    def delete_last(self):
        """
        deletes the last character of the text
        :return: None
        """
        self.text = self.text[:-1]
        self.update_field()

    def get_text(self):
        """
        it gives the current text of the field
        :return: self.text: str
        """
        return self.text

    def is_empty(self):
        """
        tells if the field is empty
        :return: bool
        """
        return self.text == ""

    def text_color(self, color: tuple):
        """
        sets the color for the text
        :param color: tuple
        :return: None
        """
        self.text_color = color

    def base_color(self, color: tuple):
        """
        sets the color of the base field color
        :param color:
        :return: None
        """
        self.base_color = color

    def event_handler(self, event: pygame.event.Event):
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
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.delete_last()
            else:
                self.write(event.unicode)


class InputFieldNumbers(InputField):
    def __init__(self,
                 WIN: pygame.Surface,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 base_color: tuple[int, int, int]=(255, 255, 255),
                 text_color: tuple[int, int, int]=BLACK,
                 **kwargs):
        super().__init__(WIN, x, y, w, h, base_color, text_color, **kwargs)

        self.key_num = {
            "normal": {
                0: 48,
                1: 49,
                2: 50,
                3: 51,
                4: 52,
                5: 53,
                6: 54,
                7: 55,
                8: 56,
                9: 57
            },
            "num_pad": {
                0: 1073741922,
                1: 1073741913,
                2: 1073741914,
                3: 1073741915,
                4: 1073741916,
                5: 1073741917,
                6: 1073741918,
                7: 1073741919,
                8: 1073741920,
                9: 1073741921
            }
        }

        self.update_field()

    def event_handler(self, event):
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
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key in self.key_num["normal"].values() or self.key_num["num_pad"].values():
                # check for normal 0-9 values
                if event.key in self.key_num["normal"].values():
                    for char_value in list(self.key_num["normal"].values()):
                        if char_value == event.key:
                            self.write(str(list(self.key_num["normal"].values()).index(char_value)))
                # check for numpad input 0-9
                elif event.key in self.key_num["num_pad"].values():
                    for char_value in list(self.key_num["num_pad"].values()):
                        if char_value == event.key:
                            self.write(str(list(self.key_num["num_pad"].values()).index(char_value)))
            # delete last character from the text
            if event.key == pygame.K_BACKSPACE:
                self.delete_last()


class InputFieldLetters(InputField):
    def __init__(self,
                 WIN: pygame.Surface,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 base_color: tuple[int, int, int]=(255, 255, 255),
                 text_color: tuple[int, int, int]=BLACK,
                 **kwargs):
        super().__init__(WIN, x, y, w, h, base_color, text_color, **kwargs)

        self.update_field()

    def event_handler(self, event: pygame.event.Event):
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
        if event.type == pygame.KEYDOWN and self.focused:
            if event.key == pygame.K_BACKSPACE:
                self.delete_last()
            elif str(event.unicode).startswith("\t") or str(event.unicode).startswith("\r"):
                pass
            elif event.unicode != "" and not str(event.unicode).startswith("\t") or not str(event.unicode).startswith("\r"):
                self.write(event.unicode)
