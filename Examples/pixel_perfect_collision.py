from PygameHelper.utils import pixel_perfect_collision, rectangle_collision
from PygameHelper.constants import *
import sys
import pygame
from pygame.locals import *


# define display surface
W, H = 1920, 1080

# initialise display
pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((W, H))
FPS = 120


obstacle = pygame.image.load("assets/obstacle.png").convert_alpha()
obstacle_mask = pygame.mask.from_surface(obstacle)
obstacle_rect = obstacle.get_rect()
ox = W//2 - obstacle_rect.center[0]
oy = H//2 - obstacle_rect.center[1]

green_blob = pygame.image.load("assets/green_blob.png").convert_alpha()
orange_blob = pygame.image.load("assets/orange_blob.png").convert_alpha()
blob_mask = pygame.mask.from_surface(green_blob)
blob_rect = green_blob.get_rect()
blob_color = green_blob

# main loop
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

    if rectangle_collision(obstacle_rect, (ox, oy), blob_rect, pygame.mouse.get_pos()):
        if pixel_perfect_collision(obstacle, (ox, oy), green_blob, pygame.mouse.get_pos()):
            blob_color = orange_blob
        else:
            blob_color = green_blob

    WIN.fill(BLACK)
    WIN.blit(obstacle, (ox, oy))
    WIN.blit(blob_color, pygame.mouse.get_pos())

    pygame.display.update()
