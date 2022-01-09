from math import sin, cos, radians
import PygameHaze as pgh
import pygame
import time
import sys


class Game:
    def __init__(self):
        self.W: int = 750
        self.H: int = 750
        self.WIN: pygame.surface.Surface = pygame.display.set_mode((self.W, self.H))

        self.running: bool = True
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        # values taken from https://en.wikipedia.org/wiki/Maurer_rose
        self.n: int = 6
        self.d: int = 71

        self.max_rad: int = 250
        self.breath = lambda: pgh.remap(sin(time.time()), -1, 1, -20, 20)
        # self.breath = lambda: 0  # uncomment this if you don't want the breathing in the rose

        # transfer the 0, 0 of the screen to the center (at least how PygameHaze sees it)
        pgh.draw.translate(self.W//2, self.H//2)

        pygame.display.set_caption("Maurer Rose aka mathematical roses")

    def event_handler(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

    def draw(self) -> None:
        self.WIN.fill(pgh.BLACK)
        pgh.draw.beginShape(self.WIN)
        breath = self.breath()
        for i in range(360):
            k = radians(i * self.d)
            r = self.max_rad * sin(self.n*k) + breath
            pgh.draw.vertex(r * cos(k), r * sin(k))
        pgh.draw.endShape(fill=False, color=pgh.WHITE, closed=True, width=1)
        pygame.display.update()

    def run(self) -> None:
        while self.running:
            self.clock.tick(self.FPS)
            self.event_handler()
            self.draw()


def run():
    game = Game()
    game.run()


if __name__ == '__main__':
    run()
