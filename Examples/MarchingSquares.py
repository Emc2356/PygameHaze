import PygameHaze as pgh
from math import ceil
import numpy as np
import pygame
import sys


pgh.noise.init()


class Game:
    def __init__(self):
        self.W: int = 700
        self.H: int = 700
        self.WIN: pygame.surface.Surface = pygame.display.set_mode((self.W, self.H))

        self.res = 5

        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        self.columns = int(self.H // self.res)
        self.rows = int(self.W // self.res)

        self.inc = 0.03

        # due to the fact that re-allocating memory for arrays can be expensive we allocate it only once
        self.perlin_values: np.ndarray = np.ndarray((self.columns * self.rows,), dtype=np.float64)

        # this is what we are going to pass into the perlin noise function,
        # it is setup so it is [x, y, z] were x, y are based on the index * 0.1 and the z changes overtime based on zoff_inc
        self.index_data: np.ndarray = np.zeros((self.columns * self.rows, 3), dtype=np.float64)
        # having all of the data from a nested loop into a numpy array

        for i in range(self.columns):
            for j in range(self.rows):
                self.index_data[j + i*self.columns] = j * 0.05, i * 0.05, 0
                
        pygame.display.set_caption("Marching Squares with perlin noise")

    def update(self) -> None:
        pgh.noise.from_array(self.index_data, 3, self.perlin_values)

        # formula to go from one range to another:
        # ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2
        # after some simplification we get this:
        # n * 2 - 1
        np.multiply(self.perlin_values, 2, self.perlin_values)
        np.subtract(self.perlin_values, 1, self.perlin_values)

        self.index_data[:, 2] += self.inc

    def event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def draw(self) -> None:
        self.WIN.fill((0, 0, 0))

        for i in range(1, self.columns - 1):
            for j in range(1, self.rows - 1):
                y = i * self.res
                x = j * self.res
                a = x, y + self.res * 0.5
                b = x + self.res * 0.5, y + self.res
                c = x + self.res, y + self.res * 0.5
                d = x + self.res * 0.5, y
                state = (
                    ceil(self.perlin_values[j   + (i  ) * self.columns]) * 8 +
                    ceil(self.perlin_values[j   + (i+1) * self.columns]) * 4 +
                    ceil(self.perlin_values[j+1 + (i+1) * self.columns]) * 2 +
                    ceil(self.perlin_values[j+1 + (i  ) * self.columns]) * 1
                )
                if state == 1:
                    pygame.draw.line(self.WIN, (255, 255, 255), c, d, 1)
                    continue
                if state == 2:
                    pygame.draw.line(self.WIN, (255, 255, 255), b, c, 1)
                    continue
                if state == 3:
                    pygame.draw.line(self.WIN, (255, 255, 255), b, d, 1)
                    continue
                if state == 4:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, b, 1)
                    continue
                if state == 5:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, d, 1)
                    pygame.draw.line(self.WIN, (255, 255, 255), b, c, 1)
                    continue
                if state == 6:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, c, 1)
                    continue
                if state == 7:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, d, 1)
                    continue
                if state == 8:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, d, 1)
                    continue
                if state == 9:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, c, 1)
                    continue
                if state == 10:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, b, 1)
                    pygame.draw.line(self.WIN, (255, 255, 255), c, d, 1)
                    continue
                if state == 11:
                    pygame.draw.line(self.WIN, (255, 255, 255), a, b, 1)
                    continue
                if state == 12:
                    pygame.draw.line(self.WIN, (255, 255, 255), b, d, 1)
                    continue
                if state == 13:
                    pygame.draw.line(self.WIN, (255, 255, 255), b, c, 1)
                    continue
                if state == 14:
                    pygame.draw.line(self.WIN, (255, 255, 255), c, d, 1)
                    continue

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.clock.tick(self.FPS)
            self.event_handler()
            self.update()
            self.draw()


def run():
    game = Game()
    game.run()


if __name__ == '__main__':
    run()
