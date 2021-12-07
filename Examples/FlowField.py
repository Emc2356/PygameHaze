from typing import List, Tuple
import PygameHelper as pgh
import pygame.gfxdraw
import itertools
import pygame
import random
import math
import sys


pgh.noise.init()  # initialize the perlin noise module


class Game:
    def __init__(self):
        self.W: int = 1200
        self.H: int = 700
        self.WIN: pygame.surface.Surface = pygame.display.set_mode((self.W, self.H))

        self.w: int = 10
        self.rows: int = self.W // self.w
        self.columns: int = self.H // self.w

        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        # create all of the Vectors from the start so i can use the .from_polar method as it is not a staticmethod
        self.flowfield: List[pygame.math.Vector2] = [pygame.math.Vector2(1, 0) for _ in range(self.columns * self.rows)]

        self.zoff: float = 0  # we are going to look the perlin noise slice by slice (moving in the z axis)
        self.zoff_inc: float = 0.03  # how fast we are moving throw "time"

        self.particles: List[Tuple[pygame.math.Vector2, pygame.math.Vector2, pygame.math.Vector2]] = []

        self.PARTICLE_COUNT: int = 2500
        for _ in range(self.PARTICLE_COUNT):
            p = pygame.math.Vector2(random.randint(0, self.W), random.randint(0, self.H))
            self.particles.append((p, pygame.math.Vector2(), pygame.math.Vector2(p)))

        self.alpha: int = 20  # the alpha value that each line will have

        self.last_update_time: int = -500

        self.octave_count: int = 4

        self.total = 0

    def update(self) -> None:
        # calculate the Vectors

        # it is the same as [[... for j in range(self.rows] for i in range(self.columns)] but cleaner
        for i, j in itertools.product(range(self.columns), range(self.rows)):
            self.flowfield[j + i * self.columns].from_polar(
                (1, math.degrees(pgh.noise(j * 0.1, i * 0.1, self.zoff) * pgh.TWO_PI * 4))
            )
        self.zoff += self.zoff_inc

        self.total += self.rows * self.columns

    def event_handler(self) -> None:
        current_time = pygame.time.get_ticks()
        if current_time // 1000 > self.last_update_time // 1000:
            pygame.display.set_caption(
                ", ".join([
                    f"FlowField with Perlin noise ",
                    f"(FPS={self.clock.get_fps():.1f}",
                    f"TARGET_FPS={self.FPS}",
                    f"SIZE={(self.W, self.H)}",
                    f"PARTICLE_COUNT={self.PARTICLE_COUNT}",
                    f"CELL_SIZE={self.w}",
                    f"OCTAVE_COUNT={self.octave_count}",
                    f"AVG_CALLS_PER_SEC={self.total / (self.zoff / self.zoff_inc) * self.clock.get_fps():.0f})"
                ])
            )
            self.last_update_time = current_time
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.WIN.fill((0, 0, 0))
                    self.particles.clear()
                    self.zoff = 0
                    self.octave_count = 4
                    pgh.noise.detail(self.octave_count)
                    for _ in range(self.PARTICLE_COUNT):
                        p = pygame.math.Vector2(random.randint(0, self.W), random.randint(0, self.H))
                        self.particles.append((p, pygame.math.Vector2(), pygame.math.Vector2(p)))
                elif event.key == pygame.K_UP:
                    self.octave_count += 1
                    pgh.noise.detail(self.octave_count)
                elif event.key == pygame.K_DOWN:
                    self.octave_count = self.octave_count - 1 if self.octave_count > 1 else 1
                    pgh.noise.detail(self.octave_count)

    def draw(self) -> None:
        # position, velocity, previous_position
        for p, v, pp in self.particles:
            i, j = int(p.y // self.w), int(p.x // self.w)
            v += self.flowfield[j + i * self.columns]
            if v.magnitude_squared() > 16: v.scale_to_length(4)
            p += v

            # edge wrapping
            if p.x > self.W:
                p.x = 0
                pp.x = p.x
            if p.x < 0:
                p.x = self.W
                pp.x = p.x
            if p.y > self.H:
                p.y = 0
                pp.y = p.y
            if p.y < 0:
                p.y = self.H
                pp.y = p.y

            # using pygame.gfxdraw because it supports alpha values
            pygame.gfxdraw.line(self.WIN, int(p[0]), int(p[1]), int(pp[0]), int(pp[1]), (255, 255, 255, self.alpha))
            pp.update(p)

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.clock.tick(self.FPS)
            self.update()
            self.event_handler()
            self.draw()


def run():
    game = Game()
    game.run()


if __name__ == '__main__':
    run()
