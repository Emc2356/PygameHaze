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
colorama package but in a optional manner
"""

try:
    import colorama
except ImportError:
    class colorama:
        class Fore:
            BLACK: str = ""
            BLUE: str = ""
            CYAN: str = ""
            GREEN: str = ""
            LIGHTBLACK_EX: str = ""
            LIGHTBLUE_EX: str = ""
            LIGHTCYAN_EX: str = ""
            LIGHTGREEN_EX: str = ""
            LIGHTMAGENTA_EX: str = ""
            LIGHTRED_EX: str = ""
            LIGHTWHITE_EX: str = ""
            LIGHTYELLOW_EX: str = ""
            MAGENTA: str = ""
            RED: str = ""
            RESET: str = ""
            WHITE: str = ""
            YELLOW: str = ""

        class Style:
            BRIGHT: str = ""
            DIM: str = ""
            NORMAL: str = ""
            RESET_ALL: str = ""

        class Back:
            BLACK: str = ""
            BLUE: str = ""
            CYAN: str = ""
            GREEN: str = ""
            LIGHTBLACK_EX: str = ""
            LIGHTBLUE_EX: str = ""
            LIGHTCYAN_EX: str = ""
            LIGHTGREEN_EX: str = ""
            LIGHTMAGENTA_EX: str = ""
            LIGHTRED_EX: str = ""
            LIGHTWHITE_EX: str = ""
            LIGHTYELLOW_EX: str = ""
            MAGENTA: str = ""
            RED: str = ""
            RESET: str = ""
            WHITE: str = ""
            YELLOW: str = ""
