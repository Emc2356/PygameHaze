import pygame
import PygameHaze as pgh


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))

pygame.display.set_caption("InputFieldNumbers")

field = pgh.InputFieldNumbers(
    250, 250, 300, 100, anchor=pgh.CENTER  # x  # y  # w  # h  # anchor
)

while True:
    for event in pygame.event.get():
        field.event_handler(event)
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            quit(-1)

    WIN.fill((30, 30, 30))
    field.draw(WIN)
    pygame.display.update()
