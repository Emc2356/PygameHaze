from typing import List, Tuple
import PygameHelper as pgh
import pygame.gfxdraw
import itertools
import pygame
import random
import sys


class Game:
    def __init__(self):
        pygame.display.set_caption("FlowField with Perlin noise")

        self.W: int = 600
        self.H: int = 400
        self.WIN: pygame.surface.Surface = pygame.display.set_mode((self.W, self.H))

        self.w: int = 25
        self.rows: int = self.W // self.w + 1
        self.columns: int = self.H // self.w + 1

        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        self.flowfield: List[pgh.Vector] = []
        self.zoff: float = 0

        self.particles: List[Tuple[pgh.Vector, pgh.Vector, pgh.Vector]] = []
        for _ in range(500):
            p = pgh.Vector(random.randint(0, self.W), random.randint(0, self.H))
            self.particles.append((p, pgh.Vector(), p.copy()))

        self.alpha: int = 20

    def update(self) -> None:
        # calculate the Vectors
        self.flowfield.clear()
        # it is the same as [[... for j in range(self.rows] for i in range(self.columns)]
        for i, j in itertools.product(range(self.columns), range(self.rows)):
            self.flowfield.append(
                pgh.Vector.from_angle(pgh.noise(j*0.1, i*0.1, self.zoff) * pgh.TWO_PI * 4)
            )
        self.zoff += 0.03

    def event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def draw(self) -> None:
        for p, v, pp in self.particles:
            i, j = int(p.y//self.w), int(p.x//self.w)
            p.add(v.add(self.flowfield[j + i*self.columns]).limit(4))

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

            # using pygame.gfxdraw cause it supports alpha values
            pygame.gfxdraw.line(self.WIN, int(p[0]), int(p[1]), int(pp[0]), int(pp[1]), (255, 255, 255, self.alpha))
            pp.update(p)

        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.clock.tick(self.FPS)
            self.event_handler()
            self.update()
            self.draw()


Game().run()
