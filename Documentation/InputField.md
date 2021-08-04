# inputField

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/Pygame-Widgets)

#### this is a class made for creating simple inputFields with the [pygame](https://www.pygame.org)
> this are the mandatory arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `WIN` | the surface that the button is going to be drawn in | - |
| `x` | the x position of the button | - |
| `y` | the x position of the button | - |
| `w` | the width of the button | - |
| `h` | the height of the button | - |
> this are the optional arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `inactive_color` | the color that is used for the outline when the button is not focused | (255, 0, 0) |
| `active_color` | the color that is used for the outline when the button is focused | (0, 255, 0) |
| `outline` | how thick will the outline be that indicates if the button is focused or not | 2 |
| `MAX` | how many characters are allowed to be in the field at one time(0 is no limit) | 0 |
| `anchor` | the alignment of the x, y positions | topleft | 
| `antialias` | if the text is going to be antialiased | True |
| `text_color` | the color of the text | (0, 0, 0) |
| `font_type` | the font that is going to be used | "comicsans" |
| `font_size` | the size of the font that is going to be used | 60 |

# Example code
```python
from PygameHelper.constants import *
import pygame
from PygameHelper import InputField


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))

field = InputField(
    WIN,            # WIN
    250,            # x
    250,            # y
    300,            # w
    100,            # h
    anchor=CENTER   # anchor
)

while True:
    for event in pygame.event.get():
        field.event_handler(event)
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)

    WIN.fill((30, 30, 30))
    field.draw()
    pygame.display.update()

```

contributions: 
---
> Pull requests are welcome! For major refactors,
> please open an issue first to discuss what you would like to improve.
> Feel free to create a fork of this repository and use the code for any noncommercial purposes.