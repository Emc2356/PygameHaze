from typing import List, Tuple
import PygameHaze as pgh
import pygame.gfxdraw
import numpy as np  # numpy to get a better performance with the noise.from_array as it excepts ndarray
import pygame
import random
import sys


pgh.noise.init()  # initialize the perlin noise module
# if numba isn't found no function will be jitted


class FlowField:
    def __init__(self):
        self.W: int = 1200
        self.H: int = 700
        self.WIN: pygame.surface.Surface = pygame.display.set_mode((self.W, self.H))

        self.w: int = 5  # size for each cell in our flowfield
        self.rows: int = self.W // self.w
        self.columns: int = self.H // self.w

        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        self.zoff_inc: float = 0.03  # how fast we are moving through "time"

        # a basic vector array with numpy were [:, 0] is x and [:, 1] is y
        self.perlin_vectors: np.ndarray = np.ndarray(
            (self.columns * self.rows, 2), dtype=np.float64
        )

        # due to the fact that re-allocating memory for arrays can be expensive we allocate it only once
        self.perlin_values: np.ndarray = np.ndarray(
            (self.columns * self.rows,), dtype=np.float64
        )

        # this is what we are going to pass into the perlin noise function,
        # it is setup so it is [x, y, z] were x, y are based on the index * 0.1 and the z changes overtime based on zoff_inc
        self.index_data: np.ndarray = np.zeros(
            (self.columns * self.rows, 3), dtype=np.float64
        )
        # having all of the data from a nested loop into a numpy array

        for i in range(self.columns):
            for j in range(self.rows):
                self.index_data[j + i * self.columns] = (j * 0.1, i * 0.1, 0)

        self.particles: List[
            Tuple[pygame.math.Vector2, pygame.math.Vector2, pygame.math.Vector2]
        ] = []

        self.PARTICLE_COUNT: int = 2500
        for _ in range(self.PARTICLE_COUNT):
            p = pygame.math.Vector2(
                random.randint(0, self.W), random.randint(0, self.H)
            )
            self.particles.append((p, pygame.math.Vector2(), pygame.math.Vector2(p)))

        self.alpha: int = 20  # the alpha value that each line will have

        # /!\ not important
        self.last_update_time: int = -500

        self.total = 0

    def update(self) -> None:
        # create vectors based on the perlin noise values with polar to cartesian coordinate transformation
        # x = r * cos(θ)
        # y = r * sin(θ)
        # formula for the angle (θ): noise_value * pi * 2 * 4
        pgh.noise.from_array(self.index_data, 3, out=self.perlin_values)

        np.multiply(self.perlin_values, pgh.PI * 2 * 4, out=self.perlin_values)

        # we dont need to multiply by r (radius) because we already know that it is 1
        np.cos(self.perlin_values, out=self.perlin_vectors[:, 0])
        np.sin(self.perlin_values, out=self.perlin_vectors[:, 1])

        self.index_data[:, 2] += self.zoff_inc  # move through "time" based in zoff_inc

        # /!\ for stats
        self.total += self.rows * self.columns

        current_time = pygame.time.get_ticks()
        if current_time // 1000 > self.last_update_time // 1000:
            pygame.display.set_caption(
                f"FlowField with Perlin noise "
                + ", ".join(
                    [
                        f"(FPS={self.clock.get_fps():.1f}",
                        f"TARGET_FPS={self.FPS}",
                        f"SIZE={(self.W, self.H)}",
                        f"PARTICLE_COUNT={self.PARTICLE_COUNT}",
                        f"CELL_SIZE={self.w}",
                        f"AVG_CALLS_PER_SEC={self.total / (self.index_data[0, 2] / self.zoff_inc) * self.clock.get_fps():.0f})",
                    ]
                )
            )
            self.last_update_time = current_time

    def event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.WIN.fill((0, 0, 0))
                    self.index_data[:, 2] = 0  # reset the "time"
                    self.particles.clear()
                    for _ in range(self.PARTICLE_COUNT):
                        p = pygame.math.Vector2(
                            random.randint(0, self.W), random.randint(0, self.H)
                        )
                        self.particles.append(
                            (p, pygame.math.Vector2(), pygame.math.Vector2(p))
                        )

    def draw(self) -> None:
        # position, velocity, previous_position
        for p, v, pp in self.particles:
            i, j = int(p.y // self.w), int(
                p.x // self.w
            )  # find the particle's location in the flowfield
            # formula for translate 2D indexes to 1D: row + column * column_count
            v += self.perlin_vectors[j + i * self.columns]
            if v.magnitude_squared() > 16:
                v.scale_to_length(4)
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
            pygame.gfxdraw.line(
                self.WIN,
                int(p[0]),
                int(p[1]),
                int(pp[0]),
                int(pp[1]),
                (255, 255, 255, self.alpha),
            )
            pp.update(p)

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.clock.tick(self.FPS)
            self.event_handler()
            self.update()
            self.draw()


def run():
    flowfield = FlowField()
    flowfield.run()


if __name__ == "__main__":
    run()
