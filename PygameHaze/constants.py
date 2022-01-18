"""
some constants and useful things
"""

from typing import Tuple, List

import math


# some of this is taken from https://github.com/ddorn/GUI
# colors have also alpha
BLACK: Tuple[int, int, int, int] = (0, 0, 0, 255)
WHITE: Tuple[int, int, int, int] = (255, 255, 255, 255)
BLUE: Tuple[int, int, int, int] = (30, 144, 255, 255)
TRUE_BLUE: Tuple[int, int, int, int] = (0, 0, 255, 255)
PURPLE: Tuple[int, int, int, int] = (155, 89, 182, 255)
RED: Tuple[int, int, int, int] = (255, 0, 0, 255)
GREEN: Tuple[int, int, int, int] = (60, 179, 113, 255)
DK_GREEN: Tuple[int, int, int, int] = (46, 139, 87, 255)
ORANGE: Tuple[int, int, int, int] = (230, 140, 30, 255)
GREY: Tuple[int, int, int, int] = (128, 128, 128, 255)
DARK_GREY: Tuple[int, int, int, int] = (30, 30, 30, 255)
LIGHT_GREY: Tuple[int, int, int, int] = (192, 192, 192, 255)
PINK: Tuple[int, int, int, int] = (255, 51, 153, 255)
FLASH_GREEN: Tuple[int, int, int, int] = (153, 255, 0, 255)
NAVY: Tuple[int, int, int, int] = (0, 0, 128, 255)
GOLD: Tuple[int, int, int, int] = (255, 214, 0, 255)
WHITESMOKE: Tuple[int, int, int, int] = (245, 245, 245, 255)

# from https://flatuicolors.com/ :D
TURQUOISE: Tuple[int, int, int, int] = (26, 188, 156, 255)
YELLOW: Tuple[int, int, int, int] = (241, 196, 15, 255)
CONCRETE: Tuple[int, int, int, int] = (149, 165, 166, 255)
PUMPKIN: Tuple[int, int, int, int] = (211, 84, 0, 255)
NICE_BLUE: Tuple[int, int, int, int] = (52, 152, 219, 255)
MIDNIGHT_BLUE: Tuple[int, int, int, int] = (44, 62, 80, 255)


COLORS: List[Tuple[int, int, int, int]] = [
    BLACK,
    WHITE,
    BLUE,
    TRUE_BLUE,
    PURPLE,
    RED,
    GREEN,
    DK_GREEN,
    ORANGE,
    GREY,
    DARK_GREY,
    LIGHT_GREY,
    PINK,
    FLASH_GREEN,
    NAVY,
    GOLD,
    TURQUOISE,
    YELLOW,
    CONCRETE,
    PUMPKIN,
    NICE_BLUE,
    MIDNIGHT_BLUE,
]


# some alignments that are used
CENTER: str = "center"
TOPLEFT: str = "topleft"
BOTTOMLEFT: str = "bottomleft"
TOPRIGHT: str = "topright"
BOTTOMRIGHT: str = "bottomright"
MIDTOP: str = "midtop"
MIDLEFT: str = "midleft"
MIDBOTTOM: str = "midbottom"
MIDRIGHT: str = "midright"

# some common pi values
PI: float = math.pi
TAU: float = math.tau
TWO_PI: float = math.pi * 2
HALF_PI: float = math.pi / 2
QUARTER_PI: float = math.pi / 4


__all__ = [
    "BLACK",
    "WHITE",
    "BLUE",
    "TRUE_BLUE",
    "PURPLE",
    "RED",
    "GREEN",
    "DK_GREEN",
    "ORANGE",
    "GREY",
    "DARK_GREY",
    "LIGHT_GREY",
    "PINK",
    "FLASH_GREEN",
    "NAVY",
    "GOLD",
    "WHITESMOKE",
    "TURQUOISE",
    "YELLOW",
    "CONCRETE",
    "PUMPKIN",
    "NICE_BLUE",
    "MIDNIGHT_BLUE",
    "CENTER",
    "TOPLEFT",
    "BOTTOMLEFT",
    "TOPRIGHT",
    "BOTTOMRIGHT",
    "MIDTOP",
    "MIDLEFT",
    "MIDBOTTOM",
    "MIDRIGHT",
    "COLORS",
    "PI",
    "TAU",
    "TWO_PI",
    "HALF_PI",
    "QUARTER_PI",
]
