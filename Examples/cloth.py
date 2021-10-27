import os
import pygame
import PygameHelper as pgh

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

cloth = pgh.Cloth(WIN, pgh.get_cloth(os.path.join("..", "tools", "cloths", "cloth.cloth")))
rects = [
    pygame.Rect(100, 100, 100, 50),
    pygame.Rect(400, 100, 50, 100),
    pygame.Rect(125, 400, 150, 50),
    pygame.Rect(75, 300, 50, 150),
    pygame.Rect(325, 300, 50, 150)
]

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit(-1)
        if event.type == pygame.MOUSEMOTION: cloth.move_all(event.pos)

    cloth.update()
    cloth.collide(rects)
    cloth.borders()

    WIN.fill(pgh.BLACK)
    for rect in rects:
        pygame.draw.rect(WIN, pgh.RED, rect)
    cloth.draw(pgh.WHITE)
    pygame.display.update()

