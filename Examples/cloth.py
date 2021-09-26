import os
import pygame
import PygameHelper as pgh

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

cloth = pgh.Cloth(WIN, pgh.get_cloth(os.path.join("..", "tools", "cloths", "cloth.cloth")))

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit(-1)
        if event.type == pygame.MOUSEMOTION: cloth.move_all(event.pos)

    cloth.update()

    WIN.fill(pgh.BLACK)
    cloth.draw(pgh.WHITE)
    pygame.display.update()

