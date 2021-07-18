import pygame


def left_click(event: pygame.event.Event):
    """
    checks if the user has left-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            return True
    return False


def middle_click(event: pygame.event.Event):
    """
    checks if the user has middle-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 2:
            return True
    return False


def right_click(event: pygame.event.Event):
    """
    checks if the user has right-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:
            return True
    return False


def get_font(size, type="comicsans"):
    """
    it send a font back with the font type and the font size given
    :param size: int
    :param type: str
    :return: pygame.font.Font
    """
    if type.endswith(".tff"):
        font = pygame.font.Font(
            type, size
        )
        return font

    font = pygame.font.SysFont(
        type, size
    )
    return font


__all__ = [
    "left_click",
    "middle_click",
    "right_click",
    "get_font"
]
