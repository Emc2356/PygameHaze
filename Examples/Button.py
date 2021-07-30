import pygame
from PygameHelper import Button
from PygameHelper.constants import *


pygame.init()
pygame.font.init()

WIN = pygame.display.set_mode((500, 500))


button = Button(
        WIN,                                                                                    # WIN
        250,                                                                                    # x
        250,                                                                                    # y
        200,                                                                                    # w
        200,                                                                                    # h
        (255, 0, 0),                                                                            # inactive_color
        (200, 0, 0),                                                                            # hover_inactive_color
        (0, 255, 0),                                                                            # active_color
        (0, 200, 0),                                                                            # hover_active_color
        anchor=CENTER,                                                                          # anchor
        text=f"hello{LINE_SPLITTER}HELLO",                                                      # text
        on_click=lambda name, age=20: print(f"""hello my name is {name} and i am {age}"""),     # what is going to be called when the button is clicked
        on_click_args=("George", ),                                                             # the positional argument that it can accept
        on_click_kwargs={"age": 20}                                                             # the key-word argument that the function can accept
)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            quit(-1)
        button.event_handler(event)

    WIN.fill((30, 30, 30))
    button.draw()
    pygame.display.update()
