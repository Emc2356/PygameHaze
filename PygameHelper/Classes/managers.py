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

from PygameHelper.Classes import Button


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
        else:
            raise TypeError(f"the given obj is not a instance of {ButtonManager} and it is a instance of the class {type(other)}")

    def __add__(self, other) -> None:
        if isinstance(other, ButtonManager):
            self.buttons += other.buttons
        else:
            raise TypeError(f"the given obj is not a instance of {ButtonManager} and it is a instance of the class {type(other)}")

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
