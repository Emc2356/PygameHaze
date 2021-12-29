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
utilities for pygame surfaces
"""

from typing import Optional, Union, List, Tuple

from PygameHelper.types import PathType
from collections import defaultdict
from functools import lru_cache
import pygame
import math
import os


class _Data:
    frame_names: defaultdict = defaultdict(lambda: -1)


def save_frame(path: PathType, target: Optional[pygame.surface.Surface]=None, *args, **kwargs) -> int:
    """
    it saves the pixels from a pygame surface into a specified file, if unspecified it defaults to the pygame window
    :param path: the name if the image (add `-####` to let this function handle the frame count)
    :param target: the surface that the function is going to save, if it is unspecified it will default to the pygame window
    :type path: AnyPath
    :type target: pygame.Surface
    :return: int
    """
    if target is None:
        target = pygame.display.get_surface()
        if target is None:
            raise ValueError(f"target was unspecified and there is no window initialized")
    try:
        if "-####" in path.split(os.sep)[~0]:
            _Data.frame_names[path] += 1
            NStr = str(_Data.frame_names[path])
            to_add = 4 - len(NStr)
            if to_add > 0:
                NStr = "-" + "0" * to_add + NStr
            path = path.replace("-####", NStr)
        pygame.image.save(target, path)
        return 0
    except Exception as e:
        if kwargs.get("warning", True):
            from colorama import (
                Fore,
                Style
            )
            print(f"{Fore.RED}unable to save {target} due to  `{e}`{Style.RESET_ALL}")
        return 1


@lru_cache()
def load_image(path: str) -> pygame.surface.Surface:
    """
    it loads an image from a given path and it performs a .convert
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert()


@lru_cache()
def load_alpha_image(path: str) -> pygame.surface.Surface:
    """
    it loads an image from a given path and it performs a .convert_alpha
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert_alpha()


def resize_smooth_image(
        image: pygame.surface.Surface, new_size: Union[List[int], Tuple[int, int]]
) -> pygame.surface.Surface:
    """
    wrapper for pygame.transform.smoothscale
    :param image: pygame.surface.Surface
    :param new_size: Union[List[int], Tuple[int, int, int]]
    :return:
    """
    return pygame.transform.smoothscale(image, new_size)


def resize_image(image: pygame.surface.Surface, new_size: Union[List[int], Tuple[int, int]]) -> pygame.surface.Surface:
    """
    wrapper for pygame.transform.scale
    :param image: pygame.surface.Surface
    :param new_size: Union[List[int], Tuple[int, int, int]]
    :return: pygame.surface.Surface
    """
    return pygame.transform.scale(image, new_size)


def resizex(image: pygame.surface.Surface, amount: float) -> pygame.surface.Surface:
    """
    it resizes a image in both axis by the same amount
    :param image: pygame.surface.Surface
    :param amount: float
    :return: pygame.surface.Surface
    """
    return pygame.transform.scale(
        image,
        (math.floor(image.get_width() * amount), math.floor(image.get_height() * amount))
    )


class _pixel_perfect_collision:
    @staticmethod
    def from_surfaces(
            image1: pygame.surface.Surface, pos1: Tuple[int, int],
            image2: pygame.surface.Surface, pos2: Tuple[int, int]
    ) -> bool:
        """
        it is a wrapper for pygame.mask.overlap and it handles the offset
        this function is recommended to be used with rectangle collision as pixel perfect collision is really heavy
        :param image1: pygame.surface.Surface
        :param pos1: Tuple[int, int]
        :param image2: pygame.surface.Surface
        :param pos2: Tuple[int, int]
        :return: bool
        """
        return not not pygame.mask.from_surface(image2).overlap(
            pygame.mask.from_surface(image1),
            tuple(pygame.math.Vector2(pos1) - pygame.math.Vector2(pos2))
        )

    @staticmethod
    def from_masks(
            mask1: pygame.mask.Mask, image_1_pos: Tuple[int, int],
            mask2: pygame.mask.Mask, image_2_pos: Tuple[int, int]
    ) -> bool:
        """
        it is a wrapper for pygame.mask.overlap and it handles the offset
        this function is recommended to be used with rectangle collision as pixel perfect collision is really heavy
        :param mask1: pygame.mask.Mask
        :param image_1_pos: Tuple[int, int]
        :param mask2: pygame.mask.Mask
        :param image_2_pos: Tuple[int, int]
        :return: bool
        """
        return not not mask1.overlap(
            mask2,
            tuple(pygame.math.Vector2(image_1_pos) - pygame.math.Vector2(image_2_pos))
        )


setattr(_pixel_perfect_collision, "__call__", staticmethod(_pixel_perfect_collision.from_surfaces))
pixel_perfect_collision = _pixel_perfect_collision()

__all__ = [
    "save_frame", "load_image", "load_alpha_image",
    "resize_smooth_image", "resize_image", "resizex",
    "pixel_perfect_collision"
]
