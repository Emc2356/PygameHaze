# SimpleText

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHelper)

#### this is a class made for creating single-line labels with the [pygame](https://www.pygame.org)
> these are the mandatory arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `WIN` | the surface that the button is going to be drawn in | - |
| `x` | the x position of the button | - |
| `y` | the x position of the button | - |
| `text` | the text that is going to be used | - |
> these are the optional arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `anchor` | the alignment of the x, y positions | topleft | 
| `antialias` | if the text is going to be antialiased | True |
| `text_color` | the color of the text | (0, 0, 0) |
| `font_type` | the font that is going to be used | "comicsans" |
| `font_size` | the size of the font that is going to be used | 60 |

# Example code
```python
# the imports
import pygame
from PygameHelper import SimpleText
from PygameHelper.constants import *


pygame.init()
pygame.font.init()


WIN = pygame.display.set_mode((500, 500))


text = SimpleText(
    WIN,                        # WIN
    250,                        # x
    250,                        # y
    "Hello Word",               # text
    RED,                        # color
    anchor=CENTER,              # anchor
    font_size=60,               # font_size
    font_type="comicsans",      # font_type
    antialias=True              # antialias
)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill((30, 30, 30))
    text.draw()
    pygame.display.update()
```
