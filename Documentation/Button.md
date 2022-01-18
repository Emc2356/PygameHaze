# Button

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHazel)

#### this is a class made for creating button with the [pygame](https://www.pygame.org)

| Argument | Description | Default Value |
|:--------:|:-----------:|:-------------:|
| `pos` | the x, y position of the button passed in as as sequence of numbers | - |
| `size` | the size of the button passed in as a sequence of numbers | - |
| `inactive_color` | the color of the button when the button is inactive | - |
| `hover_inactive_color` | the color of the button when the button is inactive and the mouse is over it | - |
| `active_color` | the color of the button when the button is active | - |
| `hover_active_color` | the color of the button when the button is active and the mouse is over it | - |
| `border_radius` | how much will the corners will be rounded | 0 |
| `anchor` | the alignment of the x, y positions | topleft | 
| `inactive_sprite` | the sprite that is used when the button is inactive | None |
| `inactive_hover_sprite` | the sprite that is used when the button is inactive and the mouse is over the button | None |
| `active_sprite` | the sprite that is used when the button is active | None |
| `active_hover_sprite` | the sprite that is used when the button is active and the mouse is over the button | None |
| `on_click` | the function that is called when the button is clicked | None |
| `on_click_args` | the positional arguments of the function that is called when the button is clicked | None |
| `on_click_kwargs` | the key-word arguments of the function that is called when the button is clicked | None |
| `on_release` | the function that is called when the button is released | None |
| `on_release_args` | the positional arguments of the function that is called when the button is released | None |
| `on_release_kwargs` | the key-word arguments of the function that is called when the button is released | None |
| `text` | the text that is going to be rendered | "" |
| `antialias` | if the text is going to be antialiased | True |
| `text_color` | the color of the text | (0, 0, 0) |
| `font_type` | the font that is going to be used | None |
| `font_size` | the size of the font that is going to be used | 60 |

# small example

```python
import PygameHaze as pgh
import pygame


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))

pygame.display.set_caption("Button")


button = pgh.Button(
        (250, 250),                                                                      # position
        (200, 200),                                                                      # size
        (255, 0, 0),                                                                     # inactive_color
        (200, 0, 0),                                                                     # hover_inactive_color
        (0, 255, 0),                                                                     # active_color
        (0, 200, 0),                                                                     # hover_active_color
        anchor=pgh.CENTER,                                                               # anchor
        text=f"\nHELLO\nWORLD\n",                                                        # text
        on_click=lambda name, age=20: print(f"hello my name is {name} and i am {age}"),  # what is going to be called when the button is clicked
        on_click_args=("George", ),                                                      # the positional argument that it can accept
        on_click_kwargs={"age": 20},                                                     # the key-word argument that the function can accept
)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)
        button.event_handler(event)

    WIN.fill((30, 30, 30))
    button.draw(WIN)
    pygame.display.update()
```
