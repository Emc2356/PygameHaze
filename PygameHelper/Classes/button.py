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


from typing import Tuple, List, Iterable

import pygame

from PygameHelper.utils import *
from PygameHelper.constants import *
from PygameHelper.exceptions import *


class Button:
    def __init__(self,
                 WIN: pygame.surface.Surface,
                 x: int,
                 y: int,
                 w: int,
                 h: int,
                 inactive_color: Tuple[int, int, int],
                 hover_inactive_color: Tuple[int, int, int],
                 active_color: Tuple[int, int, int],
                 hover_active_color: Tuple[int, int, int],
                 **kwargs):

        """

        Parameters
        ----------
        :param WIN: pygame.surface.Surface
        :param x: int
        :param y: int
        :param w: int
        :param h: int
        :param inactive_color: Tuple[int, int, int]
        :param hover_inactive_color: Tuple[int, int, int]
        :param active_color: Tuple[int, int, int]
        :param hover_active_color: Tuple[int, int, int]
        :param kwargs: optional parameters
        """

        # get the screen to draw the button
        self.WIN: pygame.surface.Surface = WIN

        # get the positions/dimensions of the button
        self.x: int = int(x)
        self.y: int = int(y)
        self.w: int = int(w)
        self.h: int = int(h)
        self.pressed: bool = False
        self.anchor: str = kwargs.get("anchor", TOPLEFT)
        self.button_rect: pygame.Rect = pygame.Rect(1, 1, 1, 1)
        self.update(self.x, self.y, self.w, self.h)

        # get the colors
        self.inactive_color: Tuple[int, int, int] = inactive_color
        self.hover_inactive_color: Tuple[int, int, int] = hover_inactive_color
        self.active_color: Tuple[int, int, int] = active_color
        self.hover_active_color: Tuple[int, int, int] = hover_active_color
        self.color: Tuple[int, int, int] = self.active_color if self.pressed else self.inactive_color

        # get the images if there is any
        inactive_sprite = kwargs.get("inactive_sprite", None)  # the sprite that is used when the button is deactivated
        if inactive_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if inactive_sprite:
                if isinstance(inactive_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.inactive_sprite = pygame.transform.scale(inactive_sprite.convert_alpha(), (self.w, self.h))
                    else:
                        self.inactive_sprite = inactive_sprite.convert_alpha()
                elif isinstance(inactive_sprite, str):
                    if transform_scale_image:
                        self.inactive_sprite = pygame.transform.scale(
                            pygame.image.load(inactive_sprite).convert_alpha(), (self.w, self.h))
                    else:
                        self.inactive_sprite = pygame.image.load(inactive_sprite).convert_alpha()
        else:
            self.inactive_sprite = None

        inactive_hover_sprite = kwargs.get("inactive_hover_sprite", None)  # the sprite that is used when the button is deactivated
        if inactive_hover_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if inactive_hover_sprite:
                if isinstance(inactive_hover_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.inactive_hover_sprite = pygame.transform.scale(inactive_hover_sprite.convert_alpha(),
                                                                            (self.w, self.h))
                    else:
                        self.inactive_hover_sprite = inactive_hover_sprite.convert_alpha()
                elif isinstance(inactive_hover_sprite, str):
                    if transform_scale_image:
                        self.inactive_hover_sprite = pygame.transform.scale(
                            pygame.image.load(inactive_hover_sprite).convert_alpha(), (self.w, self.h))
                    else:
                        self.inactive_hover_sprite = pygame.image.load(inactive_hover_sprite).convert_alpha()
        else:
            self.inactive_hover_sprite = self.inactive_sprite

        active_sprite = kwargs.get("active_sprite", None)  # the sprite that is used when the button is activated
        if active_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if active_sprite:
                if isinstance(active_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.active_sprite = pygame.transform.scale(active_sprite.convert_alpha(), (self.w, self.h))
                    else:
                        self.active_sprite = active_sprite.convert_alpha()
                elif isinstance(active_sprite, str):
                    if transform_scale_image:
                        self.active_sprite = pygame.transform.scale(pygame.image.load(active_sprite).convert_alpha(),
                                                                    (self.w, self.h))
                    else:
                        self.active_sprite = pygame.image.load(active_sprite).convert_alpha()
        else:
            self.active_sprite = self.inactive_sprite

        active_hover_sprite = kwargs.get("active_hover_sprite", None)  # the sprite that is used when the button is activated
        if active_hover_sprite:
            transform_scale_image = kwargs.get("transform_scale_image", True)
            if active_hover_sprite:
                if isinstance(active_hover_sprite, pygame.surface.Surface):
                    if transform_scale_image:
                        self.active_hover_sprite = pygame.transform.scale(active_hover_sprite.convert_alpha(),
                                                                          (self.w, self.h))
                    else:
                        self.active_hover_sprite = active_hover_sprite.convert_alpha()
                elif isinstance(active_hover_sprite, str):
                    if transform_scale_image:
                        self.active_hover_sprite = pygame.transform.scale(
                            pygame.image.load(active_hover_sprite).convert_alpha(), (self.w, self.h))
                    else:
                        self.active_hover_sprite = pygame.image.load(active_hover_sprite).convert_alpha()
        else:
            self.active_hover_sprite = self.active_sprite

        # get the functions if the user has set any
        self.on_click = kwargs.get("on_click", None)  # the function that is called when the button is activated
        self.on_click_args = kwargs.get("on_click_args", None)  # the positional arguments of the function that is called when the button is activated
        self.on_click_kwargs = kwargs.get("on_click_kwargs", None)  # the key-word arguments of the function that is called when the button is activated
        self.on_release = kwargs.get("on_release", None)  # the function that is called when the button is deactivated
        self.on_release_args = kwargs.get("on_release_args", None)  # the positional arguments of the function that is called when the button is deactivated
        self.on_release_kwargs = kwargs.get("on_release_kwargs", None)  # the key-word arguments of the function that is called when the button is deactivated

        # get the text info
        self.text = kwargs.get("text", "")  # for multiple lines use PygameHelper.constants.LINE_SPLITTER
        self.antialias = kwargs.get("antialias", True)
        self.text_color = kwargs.get("text_color", (0, 0, 0))
        self.font_type = kwargs.get("font_type", "camicsans")
        self.font_size = kwargs.get("font_size", 60)
        self.font = get_font(self.font_size, self.font_type)

        self.kwargs = kwargs

    def _blit_multiple_lines(self, x, y, centered_x=True, centered_rect: pygame.rect.Rect=None) -> None:
        """
        it blits multiple lines on the screen
        :param x: the x position of the text
        :param y: the y position of the text
        :param centered_x: if the text is going to be x-centered
        :param centered_rect: the rect that is going to be used if centered_x is True
        :return: None
        """
        if centered_x and not centered_rect:
            raise MissingRequiredArgument(f"""in the "_blit_multiple_lines method the centered_rect is missing.""")
        height = self.font.get_height()
        lines = self.text.split(LINE_SPLITTER)
        for i, text in enumerate(lines):
            rendered_text_surface = self.font.render(text, self.antialias, self.text_color)

            if centered_x:
                self.WIN.blit(rendered_text_surface, (centered_rect.centerx - rendered_text_surface.get_width()/2, y + (i * height)))

            else:
                self.WIN.blit(rendered_text_surface, (x, y + (i * height)))

    def update(self, x: int, y: int, w: int, h: int) -> None:
        """
        it reinitialise the button rect

        Parameters:
        -----------
        :param x: the x position of the button
        :param y: the y position of the button
        :param w: the width of the button
        :param h: the height of the button
        :return: None
        """
        try:
            self.button_rect = pygame.Rect(x, y, w, h)
            self.button_rect.__setattr__(self.anchor, (x, y))
        except AttributeError:
            raise InvalidAnchor(f"""The anchor '{self.anchor}' is not a valid anchor.""")
        self.x, self.y, self.w, self.h = x, y, w, h

    def draw(self) -> None:
        """
        it draws the button on the screen
        :return: None
        """
        if self.pressed:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.color = self.hover_active_color
                sprite = self.active_hover_sprite
            else:
                self.color = self.active_color
                sprite = self.active_sprite
        else:
            if self.button_rect.collidepoint(pygame.mouse.get_pos()):
                self.color = self.hover_inactive_color
                sprite = self.inactive_hover_sprite
            else:
                self.color = self.inactive_color
                sprite = self.inactive_sprite

        pygame.draw.rect(self.WIN, self.color, self.button_rect)
        if sprite:
            self.WIN.blit(sprite, self.button_rect)

        if self.text != "":
            h = 0
            height = self.font.get_height()
            lines = self.text.split(LINE_SPLITTER)
            # check for Exceptions
            for line in lines:
                label_w = self.font.render(line, self.antialias, self.text_color).get_width()
                if label_w > self.w:
                    raise TextOfOutBounds(f"the given string: '{line}' is {label_w - self.w}pxls out of bounds in the x axis")

            for i, text in enumerate(lines):
                h += i * height

            y_to_draw_text = (self.button_rect.centery - height/2) - h/4

            self._blit_multiple_lines(0, y_to_draw_text, True, self.button_rect)

    def event_handler(self, event: pygame.event.Event) -> None:
        """
        it handles the events that the class can check
        :param event: pygame.event.Event
        :return: None
        """
        if left_click(event):
            if self.button_rect.collidepoint(event.pos):
                if self.pressed:
                    self.pressed = False

                    # call the function that is given if there is any
                    if self.on_release:
                        if self.on_release_kwargs and self.on_release_args:
                            self.on_release(*self.on_release_args, **self.on_release_kwargs)

                        elif self.on_release_args:
                            self.on_release(*self.on_release_args)

                        elif self.on_release_kwargs:
                            self.on_release(**self.on_release_kwargs)

                        else:
                            self.on_release()

                elif not self.pressed:
                    self.pressed = True

                    # call the function that is given if there is any
                    if self.on_click:
                        if self.on_click_kwargs and self.on_click_args:
                            self.on_click(*self.on_click_args, **self.on_click_kwargs)

                        elif self.on_click_args:
                            self.on_click(*self.on_click_args)

                        elif self.on_click_kwargs:
                            self.on_click(**self.on_click_kwargs)

                        else:
                            self.on_click()

    def __repr__(self):
        return f"""Button at: {self.x, self.y} | with dimensions: {self.w, self.h}{f" | with text: {self.text.replace(LINE_SPLITTER, ' ')}" if self.text != '' else ''}"""


class ButtonManager:
    def __init__(self, WIN: pygame.surface.Surface):
        self.WIN = WIN
        self.buttons = []
        self.__i = 0

    def draw(self) -> None:
        [button.draw() for button in self.buttons]

    def event_handler(self, event: pygame.event.Event) -> None:
        [button.event_handler(event) for button in self.buttons]

    def get_buttons(self) -> List[Button]:
        return self.buttons

    def add_button(self,
                   x: int,
                   y: int,
                   w: int,
                   h: int,
                   inactive_color: Tuple[int, int, int],
                   hover_inactive_color: Tuple[int, int, int],
                   active_color: Tuple[int, int, int],
                   hover_active_color: Tuple[int, int, int],
                   **kwargs) -> None:
        self.buttons.append(Button(self.WIN, x, y, w, h, inactive_color, hover_inactive_color, active_color, hover_active_color, **kwargs))

    def __getitem__(self, item) -> Button:
        return self.buttons[item]

    def __setitem__(self, key, value) -> None:
        self.buttons[key] = value

    def __delitem__(self, key) -> None:
        del self.buttons[key]

    def __iadd__(self, other) -> None:
        if isinstance(other, ButtonManager):
            self.buttons += other.buttons
            return
        raise TypeError(f"the given obj is not a instance of {ButtonManager}")

    def __add__(self, other) -> None:
        if isinstance(other, ButtonManager):
            self.buttons += other.buttons
            return
        raise TypeError(f"the given obj is not a instance of {ButtonManager}")

    def __contains__(self, item) -> bool:
        if item in self.buttons:
            return True
        return False

    def __del__(self) -> None:
        for button in self.buttons:
            del button

    def __len__(self) -> int:
        return len(self.buttons)

    def __iter__(self) -> Iterable[Button]:
        return iter(self.buttons)

    def __next__(self) -> Button:
        try:
            item = self.buttons[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __repr__(self) -> str:
        _str = "["
        for button in self.buttons:
            _str += f"{button},\n"
        _str = _str[:-2]
        _str += "]"
        return _str

    def __str__(self) -> str:
        _str = "["
        for button in self.buttons:
            _str += f"{button},\n"
        _str = _str[:-2]
        _str += "]"
        return _str

    def __bool__(self) -> bool:
        return len(self) > 0

    def __reversed__(self) -> List[Button]:
        reversed(self.buttons)
        return self.buttons
