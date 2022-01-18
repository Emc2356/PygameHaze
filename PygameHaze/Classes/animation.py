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
a simple animation class
"""


from typing import List
from itertools import cycle

import pygame


class Animation:
    """
    Creates a animation

    Parameters:
    -----------
    x: int
        the x position of the animation
    y: int
        the y position of the animation
    delay: int
        the delay between sprites

    Methods:
    -----------
    animate():
        it animates the given sprites
    draw(pygame.surface.Surface):
        it draws the animation
    """
    def __init__(
            self, x: int, y: int,
            images: List[pygame.surface.Surface], delay: int=5
    ):
        self.x: int = x
        self.y: int = y
        self.images: cycle = cycle(images)
        self.delay: int = delay
        self.current_image: pygame.surface.Surface = next(self.images)
        self.time: int = 0

    def animate(self, dt: float=1) -> None:
        """
        it cycles throw the images
        :param dt: the delta time that the time system can use
        :type dt: float=1
        :return: None
        """
        if self.time >= self.delay:
            self.current_image = next(self.images)
            self.time = 0
        self.time += 1 * dt

    def draw(self, surface: pygame.surface.Surface) -> None:
        """
        it draws the animation to the screen
        :param surface: the surface that the animation will be drawn in
        :type surface: pygame.surface.Surface
        :return: None
        """
        surface.blit(self.current_image, (self.x, self.y))
