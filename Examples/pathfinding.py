import PygameHaze as pgh
import pygame
import time


pygame.display.set_caption("A* pathfinding algorithm")

pygame.init()

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

W, H = 600, 600
WIN = pygame.display.set_mode((W, H))

w = 15
h = 15
columns = H//h
rows = W//w
grid = [[0 for _ in range(rows)] for _ in range(columns)]

grid_surface = pygame.surface.Surface(WIN.get_size())
grid_surface.fill(pgh.WHITE)

for i in range(columns): pygame.draw.line(grid_surface, pgh.BLACK, (i * w, 0), (i * w, H), 1);pygame.draw.line(grid_surface, pgh.BLACK, (0, i * h), (W, i * h), 1)


start = None
end = None

clock = pygame.time.Clock()
fps = 60

path = []

while True:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            exit(-1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                path = []
                end = None
                start = None
                grid = [[0 for _ in range(rows)] for _ in range(columns)]
            elif event.key == pygame.K_SPACE and end is not None and start is not None:
                path = pgh.pathfinding(grid, start, end)  # it uses A* to find the optimal path

    mouse_pressed = pygame.mouse.get_pressed(3)
    mpos = pygame.math.Vector2(pygame.mouse.get_pos())
    i = int(mpos.y // h)
    j = int(mpos.x // w)
    spot = (i, j)
    if mouse_pressed[0]:
        if start is None and spot != end:
            start = (i, j)
        elif end is None and spot != start:
            end = (i, j)
        elif spot != end and spot != start:
            grid[i][j] = 1
    elif mouse_pressed[2]:
        grid[i][j] = 0
        if spot == start:
            start = None
        elif spot == end:
            end = None

    WIN.blit(grid_surface, (0, 0))

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            r = (j*w + 1, i*h + 1, w - 1, h - 1)
            if cell == 0:
                pygame.draw.rect(WIN, pgh.WHITE, r)
            else:
                pygame.draw.rect(WIN, pgh.RED, r)
    if start:
        pygame.draw.rect(WIN, pgh.ORANGE, (start[1]*w + 1, start[0]*h + 1, w - 1, h - 1))
    if end:
        pygame.draw.rect(WIN, pgh.TURQUOISE, (end[1]*w + 1, end[0]*h + 1, w - 1, h - 1))

    if path:
        for i, j in path:
            pygame.draw.rect(WIN, (0, 0, 255), [j*w + 1, i*h + 1, w - 1, h - 1])
            time.sleep(0.125)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    exit(-1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        path = []
                        end = None
                        start = None
                        grid = [[0 for _ in range(rows)] for _ in range(columns)]
                        break
            else: continue  # this else statement is triggered when the for loop doesnt hit a break statement
            break

    pygame.display.update()
