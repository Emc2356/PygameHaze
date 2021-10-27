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


import pygame
from itertools import cycle
from typing import List


class Animation:
    """
    Creates a animation

    Parameters:
    -----------
    WIN: pygame.surface.Surface
        the screen that the animation is going to be drawn in
    x: int
        the x position of the animation
    y: int
        the y position of the animation
    frames_per_image: int
        how many frames per sprite

    Methods:
    -----------
    animate():
        it animates the given sprites
    draw():
        it draws the animation
    """
    def __init__(self, WIN: pygame.surface.Surface, x: int, y: int, images: List[pygame.surface.Surface], frames_per_image: int=5):
        self.WIN: pygame.surface.Surface = WIN
        self.x: int = x
        self.y: int = y
        self.images: cycle = cycle(images)
        self.frames_per_image: int = frames_per_image
        self.current_image: pygame.surface.Surface = next(self.images)
        self.time: int = 0

    def animate(self) -> None:
        """
        it cycles throw the images
        :return: None
        """
        if self.time >= self.frames_per_image:
            self.current_image = next(self.images)
            self.time = 0
        self.time += 1

    def draw(self) -> None:
        """
        it draws the animation to the screen
        :return: None
        """
        self.WIN.blit(self.current_image, (self.x, self.y))
