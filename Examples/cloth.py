import os
import pygame
import PygameHaze as pgh

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

cloth = pgh.Cloth(pgh.read_json(os.path.join("..", "tools", "cloths", "cloth.cloth")))

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit(-1)
        if event.type == pygame.MOUSEMOTION: cloth.move_locked(event.pos)

    cloth.update()
    cloth.borders(WIDTH, HEIGHT)

    WIN.fill(pgh.BLACK)
    cloth.draw(WIN, pgh.WHITE)
    pygame.display.update()
