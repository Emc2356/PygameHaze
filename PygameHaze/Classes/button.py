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
a button class with a lot of abilities
"""


from typing import List, Tuple
from pathlib import Path

import pygame

from PygameHaze.types import *
from PygameHaze.utils import *
from PygameHaze.constants import *
from PygameHaze.exceptions import *


class Button:
    """
    Creates a button on the screen

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that the button is going to be drawn in
    x: int
        the x position of the button
    y: int
        the y position of the button
    w: int
        the width of the button
    h: int
        the height of the button
    inactive_color: Tuple[int, int, int]
        the color of the button when it is inactive
    hover_inactive_color: Tuple[int, int, int]
        the color of the button when it is inactive and the mouse is over it
    active_color: Tuple[int, int, int]
        the color of the button when it is active
    hover_active_color: Tuple[int, int, int]
        the color of the button when it is active and the mouse is over it
    **kwargs: optional parameters
        optional parameters

    Methods:
    -----------
    update():
        it updates the text and the button rect
    draw():
        it draws the button on the screen
    event_handler(pygame.event.Event):
        it handles the events
    """
    def __init__(
            self,
            pos: CoordsType,
            size: CoordsType,
            inactive_color: ColorType=WHITE,
            hover_inactive_color: ColorType=WHITESMOKE,
            active_color: ColorType=WHITE,
            hover_active_color: ColorType=WHITESMOKE,
            **kwargs
    ):
        if "surface" not in kwargs:
            kwargs["surface"] = pygame.display.get_surface()
        self.WIN: pygame.surface.Surface = kwargs["surface"]
        if not isinstance(self.WIN, pygame.surface.Surface):
            if "surface" in kwargs:
                raise ValueError(f"invalid value for the surface argument, {self.WIN}")
            else:
                raise pygame.error(f"no surface argument was passed and no pygame display is initialized")

        # get the positions/dimensions of the button
        x, y, *_ = pos
        w, h, *_ = size
        self._x: int = int(x)
        self._y: int = int(y)
        self._w: int = int(w)
        self._h: int = int(h)
        self.pressed: bool = False
        self.border_radius: int = kwargs.get("border_radius", 0)
        self.anchor: str = kwargs.get("anchor", TOPLEFT).lower()
        self._rect: pygame.Rect = pygame.Rect(x, y, w, h)

        # get the colors
        self.inactive_color: pygame.Color = pygame.Color(inactive_color)
        self.hover_inactive_color: pygame.Color = pygame.Color(hover_inactive_color)
        self.active_color: pygame.Color = pygame.Color(active_color)
        self.hover_active_color: pygame.Color = pygame.Color(hover_active_color)
        self.color: pygame.Color = self.active_color if self.pressed else self.inactive_color

        # get the images if there is any
        transform_scale_image = kwargs.get("transform_scale_image", True)

        inactive_sprite = kwargs.get("inactive_sprite", None)  # the sprite that is used when the button is deactivated
        if isinstance(inactive_sprite, pygame.surface.Surface):
            inactive_sprite = inactive_sprite.convert_alpha()
        elif isinstance(inactive_sprite, (str, Path)):
            inactive_sprite = load_alpha_image(inactive_sprite)
        if transform_scale_image and inactive_sprite is not None:
            inactive_sprite = pygame.transform.scale(inactive_sprite, (self._w, self._h))
        self.inactive_sprite = inactive_sprite

        inactive_hover_sprite = kwargs.get("inactive_hover_sprite", None)  # the sprite that is used when the button is deactivated and the mouse is over it
        if isinstance(inactive_hover_sprite, pygame.surface.Surface):
            inactive_hover_sprite = inactive_hover_sprite.convert_alpha()
        elif isinstance(inactive_hover_sprite, (str, Path)):
            inactive_hover_sprite = load_alpha_image(inactive_hover_sprite)
        if transform_scale_image and inactive_hover_sprite is not None:
            inactive_hover_sprite = pygame.transform.scale(inactive_hover_sprite, (self._w, self._h))
        self.inactive_hover_sprite = inactive_hover_sprite

        active_sprite = kwargs.get("active_sprite", None)  # the sprite that is used when the button is activated
        if isinstance(active_sprite, pygame.surface.Surface):
            active_sprite = active_sprite.convert_alpha()
        elif isinstance(active_sprite, (str, Path)):
            active_sprite = load_alpha_image(active_sprite)
        if transform_scale_image and active_sprite is not None:
            active_sprite = pygame.transform.scale(active_sprite, (self._w, self._h))
        self.active_sprite = active_sprite

        active_hover_sprite = kwargs.get("active_hover_sprite", None)  # the sprite that is used when the button is activated and the mouse is over it
        if isinstance(active_hover_sprite, pygame.surface.Surface):
            active_hover_sprite = active_hover_sprite.convert_alpha()
        elif isinstance(active_hover_sprite, (str, Path)):
            active_hover_sprite = load_alpha_image(active_hover_sprite)
        if transform_scale_image and active_hover_sprite is not None:
            active_hover_sprite = pygame.transform.scale(active_hover_sprite, (self._w, self._h))
        self.active_hover_sprite = active_hover_sprite

        self.current_sprite: pygame.surface.Surface = self.inactive_sprite if not self.pressed else self.active_sprite

        # get the functions if the user has set any
        self.on_click = kwargs.get("on_click", None)
        self.on_click_args = kwargs.get("on_click_args", ())
        self.on_click_kwargs = kwargs.get("on_click_kwargs", {})
        self.on_release = kwargs.get("on_release", None)
        self.on_release_args = kwargs.get("on_release_args", ())
        self.on_release_kwargs = kwargs.get("on_release_kwargs", {})

        # get the text info
        self._text = kwargs.get("text", "")  # for multiple lines use "\n"
        self.antialias = kwargs.get("antialias", True)
        self.text_color = kwargs.get("text_color", (0, 0, 0))
        self.font_type = kwargs.get("font_type", "camicsans")
        self.font_size = kwargs.get("font_size", 60)
        self.font = get_font(self.font_size, self.font_type)
        self.rendered_text_surfaces: List[Tuple[pygame.surface.Surface, List[int, int]]] = []

        self.update()

    @property
    def rect(self) -> pygame.Rect:
        return self._rect

    def update(self) -> None:
        """
        it updates the button's rect and surfaces (automatically getting called when you set the x, y, w, h, text)
        :return: None
        """
        try:
            self._rect = pygame.Rect(self._x, self._y, self._w, self._h)
            self._rect.__setattr__(self.anchor, (self._x, self._y))
        except AttributeError:
            raise InvalidAnchor(f"""The anchor '{self.anchor}' is not a valid anchor.""")

        self.rendered_text_surfaces = []
        font_h = self.font.get_height()
        y = self._rect.centery - ((len(self._text.split("\n")) * font_h) / 2)

        for i, text in enumerate(self._text.split("\n")):
            surf = self.font.render(text, self.antialias, self.text_color)
            pos = [self._rect.centerx - surf.get_width() / 2, y + (i * font_h)]
            self.rendered_text_surfaces.append((surf, pos))

            width = surf.get_width()
            if width > self._w:
                raise TextOfOutBounds(f"the given string: '{text}' is {width - self._w}pxls out of bounds in the x-axis")

        if self._text != "":
            h = len(self._text.split("\n"))*font_h
            if h > self._h:
                raise TextOfOutBounds(f"the text: [{self._text}] is {h - self._h}pxls out of bounds in the y-axis")

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, val: int) -> None:
        self._x = int(val)
        self.update()

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, val: int) -> None:
        self._y = int(val)
        self.update()

    @property
    def w(self) -> int:
        return self._w

    @w.setter
    def w(self, val: int) -> None:
        self._w = int(val)
        self.update()

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, val: int) -> None:
        self._h = int(val)
        self.update()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: str) -> None:
        self._text = str(text)
        self.update()

    def draw(self) -> None:
        """
        it draws the button on the screen
        :return: None
        """
        if self.current_sprite is not None:
            self.WIN.blit(self.current_sprite, self._rect)
        else:
            pygame.draw.rect(self.WIN, self.color, self._rect, border_radius=self.border_radius)

        self.WIN.blits(self.rendered_text_surfaces, False)

    def event_handler(self, event: pygame.event.Event) -> None:
        """
        it handles the events that the class can check
        :param event: pygame.event.Event
        :return: None
        """
        mousemotion = event.type == pygame.MOUSEMOTION
        if left_click(event) and self._rect.collidepoint(event.pos):
            if self.pressed and self.on_release:
                self.on_release(*self.on_release_args, **self.on_release_kwargs)
            elif not self.pressed and self.on_click:
                self.on_click(*self.on_click_args, **self.on_click_kwargs)
            self.pressed = not self.pressed
            mousemotion = True
        if mousemotion:
            if self.pressed:
                if self._rect.collidepoint(event.pos):
                    self.color = self.hover_active_color
                    self.current_sprite = self.active_hover_sprite
                else:
                    self.color = self.active_color
                    self.current_sprite = self.active_sprite
            else:
                if self._rect.collidepoint(event.pos):
                    self.color = self.hover_inactive_color
                    self.current_sprite = self.inactive_hover_sprite
                else:
                    self.color = self.inactive_color
                    self.current_sprite = self.inactive_sprite
