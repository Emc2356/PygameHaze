import PygameHaze as pgh
import pygame


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Bezier curve")

while True:
    for event in pygame.event.get():
        if (
            event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN
            and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            quit(-1)

    WIN.fill(pgh.DARK_GREY)

    pgh.draw.circle(WIN, pgh.RED, (0, 250), 3)
    pgh.draw.circle(WIN, pgh.GREEN, pygame.mouse.get_pos(), 3)
    pgh.draw.circle(WIN, pgh.GREEN, (350, 350), 3)
    pgh.draw.circle(WIN, pgh.RED, (500, 250), 3)

    pgh.draw.bezier(
        WIN, (0, 250), pygame.mouse.get_pos(),
        (350, 350), (500, 250), 10000, pgh.WHITE, 3,
    )
    pgh.draw.quadratic_bezier(
        WIN, (0, 250), pygame.mouse.get_pos(), (500, 250), 10000, pgh.RED, 3
    )
    pygame.display.update()
