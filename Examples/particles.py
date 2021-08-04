"""
a example if simple particles with somewhat realistic physics
responses with pygame rectangles
"""


import pygame
import time
import random
from PygameHelper.constants import RED, GREY
from PygameHelper import ParticleManager


pygame.init()


WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Particle example")

particles = ParticleManager(WIN)

rects = [
    pygame.Rect(100, 100, 100, 50),
    pygame.Rect(400, 100, 50, 100),
    pygame.Rect(125, 400, 150, 50),
    pygame.Rect(75, 300, 50, 150),
    pygame.Rect(325, 300, 50, 150)
]

clock = pygame.time.Clock()
FPS = 60

last_time = time.time()


while True:
    clock.tick(FPS)

    dt = time.time() - last_time
    dt *= FPS
    last_time = time.time()

    particles.shrink()  # it shrinks the particles
    particles.delete_particles()  # it deletes particles that have a size smaller than 0
    particles.collide_rects(rects)  # call this method to do collisions with rects
    particles.move(dt)  # call this method to move the particles
    particles.activate_gravity(dt)  # call this method so the particles slowly go down the dt is optional

    if pygame.mouse.get_pressed(3)[0]:
        for _ in range(5):        # unpack the mouse location
            particles.add_particle(*pygame.mouse.get_pos(), random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(0.1, 0.3), random.randrange(7, 10), (255, 255, 255), 5, 0.1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill(GREY)
    for rect in rects:
        pygame.draw.rect(WIN, RED, rect)
    particles.draw()
    pygame.display.update()
