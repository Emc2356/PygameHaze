# Cloth

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHazel)

#### this is a class made for creating cloths/ropes with the [pygame](https://www.pygame.org)
> these are the mandatory arguments

| Argument | Description | Default Value |
|:--------:|:-----------:|:-------------:|
| `WIN` | the surface that the cloth is going to be drawn in | - |
| `data` | the data that the cloth is going to be structured with | - |

> methods

| name | description | arguments |
|:-----:|:----------:|:---------:|
| `update` | it updates the cloth | dt=1 |
| `move_locked` | it moves the locked points in a given position (they keep their offsets) | pos |
| `move_all` | it moves all of the points in a given position (they keep their offsets) | pos |
| `offset_locked` | it moves the locked points by a given offset | pos |
| `offset_all` | it moves all of the points by a given offset | pos |
| `draw` | it draws the cloth | color, filled=False, width=2 |

# Example code

```python
import os
import pygame
import PygameHaze as pgh

WIDTH, HEIGHT = 700, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60

cloth = pgh.Cloth(WIN, pgh.read_json(os.path.join("..", "tools", "cloths", "cloth.cloth")))

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
```

# Cloth builder requirements
- it outputs json data that has
  - it has an array named "points" that has:
    - arrays that have an `x, y, is_locked, gravity`
  - it has an array named "connections" that has:
    - arrays that have `index_of_pt1, index_of_pt2, length_of_connection`

### A built-in cloth builder can be found in `../tools`
