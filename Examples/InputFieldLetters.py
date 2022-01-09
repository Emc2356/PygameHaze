import pygame
import PygameHazel as pgh


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))

pygame.display.set_caption("InputFieldLetters")

field = pgh.InputFieldLetters(
    WIN,                 # WIN
    250,                 # x
    250,                 # y
    300,                 # w
    100,                 # h
    anchor=pgh.CENTER    # anchor
)

while True:
    for event in pygame.event.get():
        field.event_handler(event)
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill((30, 30, 30))
    field.draw()
    pygame.display.update()
