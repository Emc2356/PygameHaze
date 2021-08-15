from PygameHelper import *
import pygame


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Custom Font")

font = Font("assets/pixel_font.png",
            size=4,
            spacing=1,
            barrier=(69, 69, 69),
            colorkey_for_char=(255, 255, 255)
)

while True:
    rendered_text = font.render(
        f"hello{LINE_SPLITTER} this is another test just for testing!! multi-line wrapping also supported.\n Also support for PygameHelper LINE_SPLITTER | i know the actual font sucks not gud at drawing",
        max_width=400
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill((30, 30, 30))
    WIN.blit(rendered_text, (50, 50))
    pygame.display.update()