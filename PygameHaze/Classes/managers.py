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
managers for some of the classes
"""


from typing import Tuple, List, Iterable

import pygame

from PygameHaze.types import *
from PygameHaze.constants import *
from PygameHaze.Classes import Button
from PygameHaze.Classes import InputField, InputFieldNumbers, InputFieldLetters
from PygameHaze.Classes import Particle
from PygameHaze.Classes import Animation


class _BaseManager:
    """
    override:
    __getitem__
    __iter__
    __next__
    __reversed__
    """
    def __init__(self, WIN: pygame.surface.Surface):
        self.WIN = WIN
        self.__items: List[any] = []
        self.__i = 0

    def __getitem__(self, item) -> any:
        pass

    def __iter__(self) -> Iterable[any]:
        pass

    def __next__(self) -> any:
        try:
            item = self.__items[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __reversed__(self) -> List[any]:
        pass

    # global method
    def __setitem__(self, key, value) -> None:
        self.__items[key] = value

    def __delitem__(self, key) -> None:
        del self.__items[key]

    def __iadd__(self, other) -> None:
        if isinstance(other, type(self)):
            self.__items += other.__items
        else:
            raise TypeError(f"the given obj is not a instance of {type(self)} and it is a instance of the class {type(other)}")

    def __add__(self, other) -> None:
        if isinstance(other, type(self)):
            self.__items += other.__items
        else:
            raise TypeError(f"the given obj is not a instance of {type(self)} and it is a instance of the class {type(other)}")

    def __contains__(self, item) -> bool:
        if item in self.__items:
            return True
        return False

    def __del__(self) -> None:
        for i in range(len(self.__items)):
            del self.__items[i]

    def __len__(self) -> int:
        return len(self.__items)

    def __repr__(self) -> str:
        _str = ""
        if self.__items:
            _str += "["
            for item in self.__items:
                _str += f"{item},\n"
            _str = _str[:-2]
            _str += "]"
        else:
            _str += "[]"
        return _str

    def __str__(self) -> str:
        _str = ""
        if self.__items:
            _str += "["
            for item in self.__items:
                _str += f"{item},\n"
            _str = _str[:-2]
            _str += "]"
        else:
            _str += "[]"
        return _str

    def __bool__(self) -> bool:
        return len(self) > 0
    

class ButtonManager(_BaseManager):
    """
    Creates a storage for the buttons

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that buttons are going to be drawn in

    Methods:
    -----------
    draw():
        it draws the buttons on the screen
    update():
        it updates the rects and the texts
    event_handler(pygame.event.Event):
        it sends the event to all of the stored buttons
    get_buttons():
        it returns a list of the buttons
    add_button(x, y, w, h, inactive_color, hover_inactive_color, active_color, hover_active_color, **kwargs):
        it adds a new button
    """
    def __init__(self, WIN: pygame.surface.Surface):
        super().__init__(WIN)
        self.__items: List[Button] = []

    def draw(self) -> None:
        [button.draw() for button in self.__items]

    def update(self) -> None:
        [button.update() for button in self.__items]

    def event_handler(self, event: pygame.event.Event) -> None:
        [button.event_handler(event) for button in self.__items]

    def get_buttons(self) -> List[Button]:
        return self.__items

    def add_button(self,
                   pos: CoordsType,
                   size: CoordsType,
                   inactive_color: ColorType,
                   hover_inactive_color: ColorType,
                   active_color: ColorType,
                   hover_active_color: ColorType,
                   **kwargs) -> None:
        self.__items.append(Button(
            pos,
            size,
            inactive_color,
            hover_inactive_color,
            active_color,
            hover_active_color,
            **kwargs,
            surface=self.WIN
        ))

    def __getitem__(self, item) -> Button:
        return self.__items[item]

    def __iter__(self) -> Iterable[Button]:
        return iter(self.__items)

    def __next__(self) -> Button:
        try:
            item = self.__items[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __reversed__(self) -> List[Button]:
        reversed(self.__items)
        return self.__items


class ParticleManager(_BaseManager):
    """
    Creates a storage for the particles with more functions

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that particles are going to be drawn in

    Methods:
    -----------
    draw():
        it draws the particles on the screen
    update(dt: float=1, rects=[]):
        it shrinks, apply gravity, move and collide with rects
    get_particles():
        it returns a list of the particles
    add_particle(x, y, vel_x, vel_y, shrink_amount, size, color, collision_tolerance, gravity):
        it adds a new particle
    """
    def __init__(self, WIN: pygame.surface.Surface):
        super().__init__(WIN)
        self.__items: List[Particle] = []

    def draw(self) -> None:
        [particle.draw(self.WIN) for particle in self.__items]

    def update(self, dt: float=1, rects: list[pygame.Rect]=[]) -> None:
        [particle.update(dt, rects) for particle in self.__items]
        self.__items = [particle for particle in self.__items if particle.size > 0]

    def get_particles(self) -> List[Particle]:
        return self.__items

    def add_particle(self,
                     x: int,
                     y: int,
                     vel_x: float,
                     vel_y: float,
                     shrink_amount: float,
                     size: float = 7,
                     color: Tuple[int, int, int] = (255, 255, 255),
                     collision_tolerance: float = 10,
                     gravity: float = 0.1) -> None:
        self.__items.append(Particle(x, y, vel_x, vel_y, shrink_amount, size, color, collision_tolerance, gravity))

    def __getitem__(self, item) -> Particle:
        return self.__items[item]

    def __iter__(self) -> Iterable[Particle]:
        return iter(self.__items)

    def __next__(self) -> Particle:
        try:
            item = self.__items[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __reversed__(self) -> List[Particle]:
        reversed(self.__items)
        return self.__items


__all__ = [
    "ButtonManager",
    "ParticleManager"
]
