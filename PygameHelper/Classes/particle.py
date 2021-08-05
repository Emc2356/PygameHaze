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


from typing import List
from typing import Tuple

import pygame
import random


class Particle:
    def __init__(self, WIN: pygame.surface.Surface, x: int, y: int, vel_x: float, vel_y: float, shrink_amount: float,
                 size: float=7, color: Tuple[int, int, int]=(255, 255, 255), collision_tolerance: float=10, gravity: float=0.1):
        self.WIN: pygame.surface.Surface = WIN
        self.x: int = x
        self.y: int = y
        self.vel_x: float = vel_x
        self.vel_y: float = vel_y
        self.shrink_amount: float = shrink_amount
        self.size: float = size
        self.color: Tuple[int, int, int] = color
        self.collision_tolerance: float = collision_tolerance
        self.gravity: float = gravity
        self.rect: pygame.Rect = None
        self.update_rect()

    def draw(self) -> None:
        pygame.draw.circle(self.WIN, self.color, (self.x, self.y), self.size)

    def shrink(self, dt: float=1) -> None:
        self.size -= self.shrink_amount * dt
        self.update_rect()

    def activate_gravity(self, dt: float):
        self.vel_y += self.gravity*dt
        self.update_rect()

    def move(self, dt: float):
        self.x += self.vel_x*dt
        self.y += self.vel_y*dt

    def update_rect(self):
        self.rect: pygame.Rect = pygame.Rect(self.x - self.size/2, self.y - self.size/2, self.size, self.size)

    def randomize_vel(self, limit_x: Tuple[float, float], limit_y: Tuple[float, float]) -> None:
        self.vel_x = random.uniform(*limit_x)
        self.vel_y = random.uniform(*limit_y)

    def collide_with_rects(self, rects: List[pygame.Rect], dt: float=1) -> None:
        for rect in rects:
            rect = rect.copy()
            rect.x -= self.collision_tolerance
            rect.y -= self.collision_tolerance
            rect.w += self.collision_tolerance*2
            rect.h += self.collision_tolerance*2
            if rect.colliderect(self.rect):
                if abs(rect.top - self.rect.bottom) < self.collision_tolerance and self.vel_y > 0:
                    self.vel_y *= (-0.75)*dt
                    self.y += (self.vel_y*2)*dt
                    self.update_rect()
                if abs(rect.bottom - self.rect.top) < self.collision_tolerance and self.vel_y < 0:
                    self.vel_y *= (-0.75)*dt
                    self.y += (self.vel_y*2)*dt
                    self.update_rect()
                if abs(rect.right - self.rect.left) < self.collision_tolerance and self.vel_x < 0:
                    self.vel_x *= (-0.75)*dt
                    self.x += (self.vel_x*2)*dt
                    self.update_rect()
                if abs(rect.left - self.rect.right) < self.collision_tolerance and self.vel_x > 0:
                    self.vel_x *= (-0.75)*dt
                    self.x += (self.vel_x*2)*dt
                    self.update_rect()

    def __repr__(self) -> str:
        return f"particle at: [{self.x}, {self.y}] with size: {self.size} with gravity: {self.gravity}"

    def __str__(self) -> str:
        return f"particle at: [{self.x}, {self.y}] with size: {self.size} with gravity: {self.gravity}"
