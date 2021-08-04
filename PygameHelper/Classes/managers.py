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


class TextManager:
    def __init__(self, WIN: pygame.surface.Surface):
        self.WIN = WIN
        self.texts = []
        self.__i = 0

    def draw(self) -> None:
        [text.draw() for text in self.texts]

    def update(self) -> None:
        [text.update() for text in self.texts]

    def get_texts(self) -> List[SimpleText or MultiLineText]:
        return self.texts

    def add_simple_text(self,
                        x: int,
                        y: int,
                        text: str,
                        color: Tuple[int, int, int]=BLACK,
                        **kwargs):
        self.texts.append(SimpleText(self.WIN, x, y, text, color, **kwargs))

    def add_multi_line_text(self,
                            x: int,
                            y: int,
                            text: str,
                            color: Tuple[int, int, int]=BLACK,
                            **kwargs):
        self.texts.append(MultiLineText(self.WIN, x, y, text, color, **kwargs))

    def __getitem__(self, item) -> SimpleText or MultiLineText:
        return self.texts[item]

    def __setitem__(self, key, value) -> None:
        self.texts[key] = value

    def __delitem__(self, key) -> None:
        del self.texts[key]

    def __iadd__(self, other) -> None:
        if isinstance(other, TextManager):
            self.texts += other.texts
        else:
            raise TypeError(f"the given obj is not a instance of {TextManager} and it is a instance of the class {type(other)}")

    def __add__(self, other) -> None:
        if isinstance(other, TextManager):
            self.texts += other.texts
        else:
            raise TypeError(f"the given obj is not a instance of {TextManager} and it is a instance of the class {type(other)}")

    def __contains__(self, item) -> bool:
        if item in self.texts:
            return True
        return False

    def __del__(self) -> None:
        for text in self.texts:
            del text

    def __len__(self) -> int:
        return len(self.texts)

    def __iter__(self) -> Iterable[SimpleText or MultiLineText]:
        return iter(self.texts)

    def __next__(self) -> SimpleText or MultiLineText:
        try:
            item = self.texts[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __repr__(self) -> str:
        _str = "["
        for text in self.texts:
            _str += f"{text},\n"
        _str = _str[:-2]
        _str += "]"
        return _str

    def __str__(self) -> str:
        _str = "["
        for text in self.texts:
            _str += f"{text},\n"
        _str = _str[:-2]
        _str += "]"
        return _str

    def __bool__(self) -> bool:
        return len(self) > 0

    def __reversed__(self) -> List[SimpleText or MultiLineText]:
        reversed(self.texts)
        return self.texts


class InputFieldManager:
    def __init__(self, WIN: pygame.surface.Surface):
        self.WIN = WIN
        self.input_fields = []
        self.__i = 0

    def draw(self) -> None:
        [text.draw() for text in self.input_fields]

    def update(self) -> None:
        [text.update() for text in self.input_fields]

    def event_handler(self, event: pygame.event.Event) -> None:
        [input_field.event_hanler(event) for input_field in self.input_fields]

    def get_input_fields(self) -> List[InputField or InputFieldNumbers or InputFieldLetters]:
        return self.input_fields

    def add_Input_field(self,
                        x: int,
                        y: int,
                        w: int,
                        h: int,
                        base_color: Tuple[int, int, int]=WHITE,
                        text_color: Tuple[int, int, int]=BLACK,
                        **kwargs):
        self.input_fields.append(InputField(self.WIN, x, y, w, h, base_color, text_color, **kwargs))

    def add_Input_field_numbers(self,
                                x: int,
                                y: int,
                                w: int,
                                h: int,
                                base_color: Tuple[int, int, int]=WHITE,
                                text_color: Tuple[int, int, int]=BLACK,
                                **kwargs):
        self.input_fields.append(InputFieldNumbers(self.WIN, x, y, w, h, base_color, text_color, **kwargs))

    def add_Input_field_letters(self,
                                x: int,
                                y: int,
                                w: int,
                                h: int,
                                base_color: Tuple[int, int, int] = WHITE,
                                text_color: Tuple[int, int, int] = BLACK,
                                **kwargs):
        self.input_fields.append(InputFieldLetters(self.WIN, x, y, w, h, base_color, text_color, **kwargs))

    def __getitem__(self, item) -> InputField or InputFieldNumbers or InputFieldLetters:
        return self.input_fields[item]

    def __setitem__(self, key, value) -> None:
        self.input_fields[key] = value

    def __delitem__(self, key) -> None:
        del self.input_fields[key]

    def __iadd__(self, other) -> None:
        if isinstance(other, InputFieldManager):
            self.input_fields += other.input_fields
        else:
            raise TypeError(f"the given obj is not a instance of {InputFieldManager} and it is a instance of the class {type(other)}")

    def __add__(self, other) -> None:
        if isinstance(other, InputFieldManager):
            self.input_fields += other.input_fields
        else:
            raise TypeError(f"the given obj is not a instance of {InputFieldManager} and it is a instance of the class {type(other)}")

    def __contains__(self, item) -> bool:
        if item in self.input_fields:
            return True
        return False

    def __del__(self) -> None:
        for text in self.input_fields:
            del text

    def __len__(self) -> int:
        return len(self.input_fields)

    def __iter__(self) -> Iterable[InputField or InputFieldNumbers or InputFieldLetters]:
        return iter(self.input_fields)

    def __next__(self) -> InputField or InputFieldNumbers or InputFieldLetters:
        try:
            item = self.input_fields[self.__i]
            self.__i += 1
        except IndexError:
            self.__i = 0
            item = self.__next__()

        return item

    def __repr__(self) -> str:
        _str = "["
        for text in self.input_fields:
            _str += f"{text},\n"
        _str = _str[:-2]
        _str += "]"
        return _str

    def __str__(self) -> str:
        _str = "["
        for text in self.input_fields:
            _str += f"{text},\n"
        _str = _str[:-2]
        _str += "]"
        return _str

    def __bool__(self) -> bool:
        return len(self) > 0

    def __reversed__(self) -> List[InputField or InputFieldNumbers or InputFieldLetters]:
        reversed(self.input_fields)
        return self.input_fields