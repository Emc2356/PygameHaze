# Animation

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHazel)

#### this is a class made for creating animations with the [pygame](https://www.pygame.org)
> these are the mandatory arguments

| Argument | Description | Default Value |
|:--------:|:-----------:|:-------------:|
| `x` | the x position of the image | - |
| `y` | the y position of the image | - |
| `images` | a list of the images that are going to be used in the animations | - |
| `delay` | how many frames one image is drawn on the screen | 5 |
| `anchor` | were the x, y is going to be placed | topleft |

# Example code

```python
from PygameHaze import Animation
from PygameHaze import load_image, resize_image_ratio,  WHITE
import pygame


pygame.init()


WIDTH, HEIGHT = 500, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("animation")

images = [resize_image_ratio(load_image(f"assets/clock/clock_{i+1}.png"), (64, 64)) for i in range(8)]
animation = Animation(WIDTH//2 - 64//2, HEIGHT//2 - 64//2, images, 5)

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
    animation.draw(WIN)
    pygame.display.update()
```
