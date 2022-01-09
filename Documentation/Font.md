# Button

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/Pygame-Widgets)

#### this is a class made for creating button with the [pygame](https://www.pygame.org)
> these are the mandatory arguments

| Argument | Description | Default Value |
|:--------:|:-----------:|:-------------:|
| `type` | the path to the font image | - |
| `size` | the size multiplier for the font | 1 |
| `barrier` | the color of the barrier between the letters | (0, 0, 0) |
| `colorkey_for_char` | the colorkey for the spritesheet | None |
| `spacing` | how much spacing per letter | 1 |

# Example code

```python
# the imports
from PygameHaze import *
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
        f"hello\n this is another test just for testing!! multi-line wrapping also supported.\n Also i know the actual font sucks not gud at drawing",
        max_width=400
    )
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill((30, 30, 30))
    WIN.blit(rendered_text, (50, 50))
    pygame.display.update()
```

# Custom Fonts
~~~
to create a custom font image you need to create a image with
the following order of the letters:
A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z,
., -, +, /, *, =, ,, [, ], (, ), {, }, ', !, ?, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
_, |, \, <, >
then beteewn the letters you are going to be a barrier with a uniqe color
put barriers only after a letter not before

PS. your image shouldnt be transparent as it is going to mess up the order as
it is going to find more pixels with the same color

for refrence go to Examples/assets/pixel_font.png
~~~

# contributions:
---
> Pull requests are welcome!
> Feel free to create a fork of this repository and use the code for any noncommercial purposes.
