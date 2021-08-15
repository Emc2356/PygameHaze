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

from PygameHelper.constants import *
from PygameHelper.Classes import Button
from PygameHelper.Classes import SimpleText, MultiLineText
from PygameHelper.Classes import InputField, InputFieldNumbers, InputFieldLetters
from PygameHelper.Classes import Particle
from PygameHelper.Classes import Animation


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
                   x: int,
                   y: int,
                   w: int,
                   h: int,
                   inactive_color: Tuple[int, int, int],
                   hover_inactive_color: Tuple[int, int, int],
                   active_color: Tuple[int, int, int],
                   hover_active_color: Tuple[int, int, int],
                   **kwargs) -> None:
        self.__items.append(Button(self.WIN, x, y, w, h, inactive_color, hover_inactive_color, active_color, hover_active_color, **kwargs))

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


class TextManager(_BaseManager):
    """
    Creates a storage for the texts

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that texts are going to be drawn in

    Methods:
    -----------
    draw():
        it draws the texts on the screen
    update():
        it updates the texts
    get_texts():
        it returns a list with the stored texts
    add_simple_text(x, y, text, color, **kwargs):
        it adds a new one-line text
    add_multi_line_text(x, y, text, color, **kwargs):
        it adds a new multi-line text
    """
    def __init__(self, WIN: pygame.surface.Surface):
        super().__init__(WIN)
        self.__items: List[SimpleText or MultiLineText] = []

    def draw(self) -> None:
        [text.draw() for text in self.__items]

    def update(self) -> None:
        [text.update() for text in self.__items]

    def get_texts(self) -> List[SimpleText or MultiLineText]:
        return self.__items

    def add_simple_text(self,
                        x: int,
                        y: int,
                        text: str,
                        color: Tuple[int, int, int]=BLACK,
                        **kwargs) -> None:
        self.__items.append(SimpleText(self.WIN, x, y, text, color, **kwargs))

    def add_multi_line_text(self,
                            x: int,
                            y: int,
                            text: str,
                            color: Tuple[int, int, int]=BLACK,
                            **kwargs) -> None:
        self.__items.append(MultiLineText(self.WIN, x, y, text, color, **kwargs))

    def __getitem__(self, item) -> SimpleText or MultiLineText:
        return self.__items[item]

    def __iter__(self) -> Iterable[SimpleText or MultiLineText]:
        return iter(self.__items)

    def __next__(self) -> SimpleText or MultiLineText:
        try:
            item = self.__items[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __reversed__(self) -> List[SimpleText or MultiLineText]:
        reversed(self.__items)
        return self.__items


class InputFieldManager(_BaseManager):
    """
    Creates a storage for the input fields

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that input fields are going to be drawn in

    Methods:
    -----------
    draw():
        it draws the input fields
    update():
        it updates the rects and the texts in the input fields
    event_handler(pygame.event.Event):
        it sends the event to the input fields
    get_input_fields():
        it returns a list with the input fields
    add_Input_field(x, y, w, h, base_color, text_color, **kwargs):
        it adds a new input field that can write anything
    add_Input_field_numbers(x, y, w, h, base_color, text_color, **kwargs):
        it adds a new input field that can accept numbers
    add_Input_field_letters(x, y, w, h, base_color, text_color, **kwargs):
        it adds a new input field that can accept numbers and letters
    """
    def __init__(self, WIN: pygame.surface.Surface):
        super().__init__(WIN)
        self.__items: List[InputField or InputFieldNumbers or InputFieldLetters] = []

    def draw(self) -> None:
        [text.draw() for text in self.__items]

    def update(self) -> None:
        [text.update() for text in self.__items]

    def event_handler(self, event: pygame.event.Event) -> None:
        [input_field.event_handler(event) for input_field in self.__items]

    def get_input_fields(self) -> List[InputField or InputFieldNumbers or InputFieldLetters]:
        return self.__items

    def add_Input_field(self,
                        x: int,
                        y: int,
                        w: int,
                        h: int,
                        base_color: Tuple[int, int, int]=WHITE,
                        text_color: Tuple[int, int, int]=BLACK,
                        **kwargs) -> None:
        self.__items.append(InputField(self.WIN, x, y, w, h, base_color, text_color, **kwargs))

    def add_Input_field_numbers(self,
                                x: int,
                                y: int,
                                w: int,
                                h: int,
                                base_color: Tuple[int, int, int]=WHITE,
                                text_color: Tuple[int, int, int]=BLACK,
                                **kwargs) -> None:
        self.__items.append(InputFieldNumbers(self.WIN, x, y, w, h, base_color, text_color, **kwargs))

    def add_Input_field_letters(self,
                                x: int,
                                y: int,
                                w: int,
                                h: int,
                                base_color: Tuple[int, int, int] = WHITE,
                                text_color: Tuple[int, int, int] = BLACK,
                                **kwargs) -> None:
        self.__items.append(InputFieldLetters(self.WIN, x, y, w, h, base_color, text_color, **kwargs))

    def __getitem__(self, item) -> InputField or InputFieldNumbers or InputFieldLetters:
        return self.__items[item]

    def __iter__(self) -> Iterable[InputField or InputFieldNumbers or InputFieldLetters]:
        return iter(self.__items)

    def __next__(self) -> InputField or InputFieldNumbers or InputFieldLetters:
        try:
            item = self.__items[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __reversed__(self) -> List[InputField or InputFieldNumbers or InputFieldLetters]:
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
    shrink():
        it shrinks the particles
    delete_particles():
        it deletes particles that have a size smaller than 0
    collide_rects(pygame_rects, DeltaTime):
        it checks for collisions with pygame rects
    update_rects():
        it updates the rects
    randomize_vels():
        it it randomizes the velocities of the particles (why did i even made this smh)
    move(DeltaTime=1):
        it moves the particle
    activate_gravity(DeltaTime=1):
        it applies the gravity to the particles
    get_particles():
        it returns a list of the particles
    add_particle(x, y, vel_x, vel_y, shrink_amount, size, color, collision_tolerance, gravity):
        it adds a new particle
    """
    def __init__(self, WIN: pygame.surface.Surface):
        super().__init__(WIN)
        self.__items: List[Particle] = []

    def draw(self) -> None:
        [text.draw() for text in self.__items]

    def shrink(self, dt: float=1) -> None:
        [text.shrink(dt) for text in self.__items]

    def delete_particles(self) -> None:
        new_particles = [particle for particle in self.__items if particle.size > 0]
        self.__items = new_particles

    def collide_rects(self, rects: List[pygame.Rect], dt: float=1) -> None:
        [particle.collide_with_rects(rects, dt) for particle in self.__items]

    def update_rects(self) -> None:
        [particle.update_rect() for particle in self.__items]

    def randomize_vels(self, limit_x: Tuple[float, float], limit_y: Tuple[float, float]) -> None:
        [particle.randomize_vel(limit_x, limit_y) for particle in self.__items]

    def move(self, dt: float=1) -> None:
        [particle.move(dt) for particle in self.__items]

    def activate_gravity(self, dt: float=1) -> None:
        [particle.activate_gravity(dt) for particle in self.__items]

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
        self.__items.append(Particle(self.WIN, x, y, vel_x, vel_y, shrink_amount, size, color, collision_tolerance, gravity))

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


class AnimationManager(_BaseManager):
    """
    Creates a storage for the animations

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that the animations are going to be drawn in

    Methods:
    -----------
    draw():
        it draws the animations on the screen
    animate():
        it animates the stored animations
    get_animations():
        it returns a list with the stored animations
    add_animation(x, y, images, frames_per_image):
        it creates a new animation
    """
    def __init__(self, WIN: pygame.surface.Surface):
        super().__init__(WIN)
        self.__items: List[Animation] = []

    def draw(self) -> None:
        [animation.draw() for animation in self.__items]

    def animate(self) -> None:
        [animation.animate() for animation in self.__items]

    def get_animations(self) -> List[Animation]:
        return self.__items

    def add_animation(self,
                      x: int,
                      y: int,
                      images: List[pygame.surface.Surface],
                      frames_per_image: int=5) -> None:
        self.__items.append(Animation(self.WIN, x, y, images, frames_per_image))

    def __getitem__(self, item) -> Animation:
        return self.__items[item]

    def __iter__(self) -> Iterable[Animation]:
        return iter(self.__items)

    def __next__(self) -> Animation:
        try:
            item = self.__items[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __reversed__(self) -> List[Animation]:
        reversed(self.__items)
        return self.__items


__all__ = [
    "ButtonManager",
    "TextManager",
    "InputFieldManager",
    "ParticleManager",
    "AnimationManager"
]
