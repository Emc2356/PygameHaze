from PygameHazel import Animation
from PygameHazel import load_image, resize_image_ratio,  WHITE
import pygame


pygame.init()


WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("animation")

images = [resize_image_ratio(load_image(f"assets/clock/clock_{i+1}.png"), (64, 64)) for i in range(8)]
animation = Animation(WIN, WIDTH//2 - 64//2, HEIGHT//2 - 64//2, images, 5)

clock = pygame.time.Clock()
FPS = 60


while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill(WHITE)
    animation.animate()
    animation.draw()
    pygame.display.update()
