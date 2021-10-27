# MIT License
#
# Copyright (c) 2021 Emc2356
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
some useful functions for pygame
and general use
"""

from typing import List, Tuple, Iterable, Generator, Union, Dict, Sequence, Set, TypeVar, Any, overload as TpOverload
from functools import lru_cache
from queue import PriorityQueue

import pygame
import json
import math

from PygameHelper.constants import *
from PygameHelper.exceptions import *

Number = Union[int, float]
NeighborOutputType = TypeVar("NeighborOutputType")


# builtins that have been changed a little for a specific purpose
# the names are going to be bad, but this isn't something that you should touch too much :)
class _CT:
    class ASPos:  # it is used for A* pathfinding
        __slots__ = "i", "j", "v"

        def __init__(self, idxs: Tuple[int, int], v: Number) -> None:
            self.i: int = idxs[0]
            self.j: int = idxs[1]
            self.v: Number = v

        @property
        def pos(self) -> Tuple[int, int]:
            return self.i, self.j

        def neighbors(self, grid: List[List["ASPos"]]) -> Generator:
            columns = len(grid)
            rows = len(grid[0])
            i = self.i
            j = self.j

            if i < columns - 1 and grid[self.i + 1][j].v == 0:
                yield grid[self.i + 1][j]

            if i > 0 and grid[self.i - 1][j].v == 0:
                yield grid[self.i - 1][j]

            if j < rows - 1 and grid[self.i][j + 1].v == 0:
                yield grid[self.i][j + 1]

            if j > 0 and grid[self.i][j - 1].v == 0:
                yield grid[self.i][j - 1]

        def __lt__(self, other):
            return False

        @TpOverload
        def __getitem__(self, idx: int) -> int: ...

        @TpOverload
        def __getitem__(self, idx: slice) -> List[int]: ...

        def __getitem__(self, idx: slice) -> Union[int, List[int]]:
            return [self.i, self.j, self.v][idx]

        def __repr__(self) -> str:
            return repr(f"${self.i} ${self.j} ${self.v}")


ASPos = _CT.ASPos


@lru_cache()
def load_image(path: str) -> pygame.surface.Surface:
    """
    it loads an image from a given path and it performs a .convert
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert()


@lru_cache()
def load_alpha_image(path: str) -> pygame.surface.Surface:
    """
    it loads an image from a given path and it performs a .convert_alpha
    :param path: str
    :return: pygame.surface.Surface
    """
    return pygame.image.load(path).convert_alpha()


def resize_smooth_image(
        image: pygame.surface.Surface, new_size: Union[List[int], Tuple[int, int]]
) -> pygame.surface.Surface:
    """
    wrapper for pygame.transform.smoothscale
    :param image: pygame.surface.Surface
    :param new_size: Union[List[int], Tuple[int, int, int]]
    :return:
    """
    return pygame.transform.smoothscale(image, new_size)


def resize_image(image: pygame.surface.Surface, new_size: Union[List[int], Tuple[int, int]]) -> pygame.surface.Surface:
    """
    wrapper for pygame.transform.scale
    :param image: pygame.surface.Surface
    :param new_size: Union[List[int], Tuple[int, int, int]]
    :return: pygame.surface.Surface
    """
    return pygame.transform.scale(image, new_size)


def resize_image_ratio(image: pygame.surface.Surface, new_size: Tuple[int, int]) -> pygame.surface.Surface:
    ratio = new_size[0] / image.get_width()
    return pygame.transform.scale(image,
                                  (math.floor(image.get_width() * ratio), math.floor(image.get_height() * ratio)))


def resizex(image: pygame.surface.Surface, amount: Number) -> pygame.surface.Surface:
    """
    it resizes a image in both axis by the same amount
    :param image: pygame.surface.Surface
    :param amount: Union[int, float]
    :return: pygame.surface.Surface
    """
    return pygame.transform.scale(image,
                                  (math.floor(image.get_width() * amount), math.floor(image.get_height() * amount)))


def left_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has left-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            return True
    return False


def middle_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has middle-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 2:
            return True
    return False


def right_click(event: pygame.event.Event) -> bool:
    """
    checks if the user has right-clicked the screen
    :param event: pygame.event.Event
    :return: bool
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:
            return True
    return False


@lru_cache()
def get_font(size, type_of_font="comicsans") -> pygame.font.Font:
    """
    it returns a font
    :param size: int
    :param type_of_font: str
    :return: pygame.font.Font
    """
    if type_of_font.endswith(".tff"):
        font = pygame.font.Font(
            type_of_font, size
        )
        return font

    font = pygame.font.SysFont(
        type_of_font, size
    )
    return font


@lru_cache()
def wrap_multi_lines(
        text: str, font: pygame.font.Font, max_width: int, max_height: int=0, antialias: bool=True
) -> List[str]:
    """
    it returns a list of strings
    :param text: str
    :param font: pygame.font.Font
    :param max_width: int
    :param max_height: int=0
    :param antialias: bool=True
    :return: List[str]
    """
    finished_lines = [""]

    for word in text.split(" "):
        w = font.render(word, antialias, BLACK).get_width()
        # check if one word is too long to fit in one line
        if w > max_width:
            raise WordTooLong(
                f"""the word: "{word}" is too long to fit in a width of: {max_width}, out of bounds by: {w - max_width}pxls""")

        if font.render(finished_lines[-1] + word, antialias, BLACK).get_width() > max_width:
            finished_lines.append(f"""{word}""")
        else:
            finished_lines[-1] += f""" {word}"""
    finished_lines[0] = finished_lines[0][1:]
    if max_height > 0:
        h = 0
        for line in finished_lines:
            h += font.render(line, antialias, BLACK).get_height()

        if h > max_height:
            raise TextOfOutBounds(
                f"""the lines: {finished_lines} are too long in the y axis by: {h - max_height}pxls""")

    return finished_lines


def blit_multiple_lines(
        x: int, y: int, lines: List[str], WIN: pygame.surface.Surface, font: pygame.font.Font,
        centered_x=False, centered_x_pos: int=None, color: Tuple[int, int, int]=(0, 0, 0)
) -> None:
    """
    it blits in a surface a list of strings
    :param x: int
    :param y: int
    :param lines: list[str]
    :param WIN: pygame.surface.Surface
    :param font: pygame.font.Font
    :param centered_x: if the text is going to be x-centered
    :param centered_x_pos: the rect that is going to be used if centered_x is True
    :param color: Tuple[int, int, int]
    :return: None
    """
    if centered_x and not centered_x_pos:
        raise MissingRequiredArgument("Missing 'centered_x_pos'")
    height = font.get_height()
    for i, text in enumerate(lines):
        rendered_text_surface = font.render(text, True, color)

        if centered_x:
            WIN.blit(rendered_text_surface, (centered_x_pos - rendered_text_surface.get_width() / 2, y + (i * height)))

        else:
            WIN.blit(rendered_text_surface, (x, y + (i * height)))


def pixel_perfect_collision(
        image_1: pygame.surface.Surface, image_1_pos: Tuple[int, int],
        image_2: pygame.surface.Surface, image_2_pos: Tuple[int, int]
) -> bool:
    """
    it is a wrapper for pygame.mask.overlap and it handles the offset
    this function is recommended to be used with rectangle collision as pixel perfect collision is really heavy
    :param image_1: pygame.surface.Surface
    :param image_1_pos: Tuple[int, int]
    :param image_2: pygame.surface.Surface
    :param image_2_pos: Tuple[int, int]
    :return: bool
    """
    offset = [image_1_pos[0] - image_2_pos[0],
              image_1_pos[1] - image_2_pos[1]]
    mask_1 = pygame.mask.from_surface(image_1)
    mask_2 = pygame.mask.from_surface(image_2)

    result = mask_2.overlap(mask_1, offset)
    if result:
        return True
    return False


@lru_cache()
def get_distance(x1: int, y1: int, x2: int, y2: int) -> float:
    """
    it returns the distance between two points
    :param x1: int
    :param y1: int
    :param x2: int
    :param y2: int
    :return: float
    """
    return math.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2))


def flatten(iterable: Iterable) -> Generator:
    """
    it takes a iterable object and it flattens the object
    :param iterable: Iterable
    :return: any
    """
    for item in iterable:
        if isinstance(item, list) or isinstance(item, tuple):
            for subitem in flatten(item):
                yield subitem
        else:
            yield item


def get_cloth(path: str) -> Dict[str, list]:
    """
    it returns the cloth data from a file
    :param path: str
    :return: Dict
    """
    with open(path, "r") as f:
        data = json.loads(f.read())
    return data


def clamp(value: Number, mini: Number, maxi: Number) -> Number:
    """
    it clamps a value between mini and maxi
    :param value: Union[int, float]
    :param mini: Union[int, float]
    :param maxi: Union[int, float]
    :return: Union[int, float]
    """
    return mini if value < mini else value if value < maxi else maxi


def remap(
        n: Number, start1: Number, stop1: Number, start2: Number, stop2: Number, within_bounds: bool = False
) -> float:
    """
    it Re-maps a number from one range to another (nothing to do with regex it is just the name)
    :param n: Union[int, float]
    :param start1: Union[int, float]
    :param stop1: Union[int, float]
    :param start2: Union[int, float]
    :param stop2: Union[int, float]
    :param within_bounds: bool
    :return: Union[int, float]
    """
    v = ((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2
    if not within_bounds:
        return v
    if start2 < stop2:
        return clamp(v, start2, stop2)
    else:
        return clamp(v, stop2, start2)


def lerp(start: Number, stop: Number, amount: Number) -> float:
    """
    Calculates a number between two numbers at a specific increment
    :param start: Union[int, float]
    :param stop: Union[int, float]
    :param amount: Union[int, float]
    :return: float
    """
    if amount > 1 or amount < 0:
        if amount > 1:
            raise ValueError(f"amount in lerp function is bigger than 1")
        if amount < 0:
            raise ValueError(f"amount in lerp function is smaller than 0")
    return amount * (stop - start) + start


def _quadratic(p1: Sequence, p2: Sequence, p3: Sequence, t: Number) -> pygame.math.Vector2:
    """
    Quadratic bezier curve (1 static, 1 control and 1 static point)
    :param p1: Sequence
    :param p2: Sequence
    :param p3: Sequence
    :param t: Union[int, float]
    :return: pygame.math.Vector2
    """
    return pygame.math.Vector2(
        lerp(lerp(p1[0], p2[0], t), lerp(p2[0], p3[0], t), t),
        lerp(lerp(p1[1], p2[1], t), lerp(p2[1], p3[1], t), t)
    )


def quadratic_bezier(p1: Sequence, p2: Sequence, p3: Sequence, delta: Number = 0.03) -> List[pygame.math.Vector2]:
    """
    Quadratic bezier curve (1 static, 1 control and 1 static point)
    :param p1: Sequence
    :param p2: Sequence
    :param p3: Sequence
    :param delta: Union[int, float]
    :return: pygame.math.Vector2
    """
    mul_am = int(1 / delta)
    return [_quadratic(p1, p2, p3, t / mul_am) for t in range(0, mul_am + 1, 1)]


def bezier(p1: Sequence, p2: Sequence, p3: Sequence, p4: Sequence, delta: Number = 0.03) -> List[pygame.math.Vector2]:
    """
    it creates a bezier curve based on 4 points (1 static, 2 control points an 1 static) aka a cubic bezier
    :param p1: Sequence
    :param p2: Sequence
    :param p3: Sequence
    :param p4: Sequence
    :param delta: Union[int, float]
    :return: List[pygame.math.Vector2]
    """
    if delta >= 1 or delta <= 0:
        if delta >= 1:
            raise ValueError(f"delta in bezier function is bigger or equal than 1")
        if delta <= 0:
            raise ValueError(f"delta in bezier function is smaller or equal than 0")
    points = []
    mul_am = int(1 / delta)
    for t in range(0, mul_am + 1, 1):
        t /= mul_am
        v1 = _quadratic(p1, p2, p3, t)
        v2 = _quadratic(p2, p3, p4, t)
        points.append(
            pygame.math.Vector2(
                lerp(v1.x, v2.x, t), lerp(v1.y, v2.y, t)
            )
        )
    return points


def _heuristic(p1: ASPos, p2: ASPos) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_neighbors(
        grid: List[List[NeighborOutputType]], target: Union[Tuple[int, int], List[int], Sequence[int]]
) -> Generator:
    """
    it returns the directly adjacent cells (it makes the assumption that it has rows of the same length)
    :param grid: List[List[Any]]
    :param target: Union[Tuple[int, int], List[int, int], Sequence[int]]
    :return: List[Any]
    """
    columns = len(grid) - 1
    rows = len(grid[0]) - 1
    oi, oj = target

    for i, j in [(oi - 1, oj), (oi, oj - 1), (oi, oj + 1), (oi + 1, oj)]:
        if not (i == oi and j == oj) and 0 <= i <= columns and 0 <= j <= rows:
            yield grid[i][j]


def get_neighbors_index(
        grid: List[List[Any]],
        target: Union[Tuple[int, int], List[int], Sequence[int]]
) -> Generator:
    """
    it returns the directly adjacent cells index (it makes the assumption that it has rows of the same length)
    :param grid: List[List[Any]]
    :param target: Union[Tuple[int, int], List[int, int], Sequence[int]]
    :return: List[Any]
    """
    columns = len(grid) - 1
    rows = len(grid[0]) - 1
    oi, oj = target

    for i, j in [(oi - 1, oj), (oi, oj - 1), (oi, oj + 1), (oi + 1, oj)]:
        if not (i == oi and j == oj) and 0 <= i <= columns and 0 <= j <= rows:
            yield i, j


def pathfinding(
        grid: List[List[int]], start: Union[List[int], Tuple[int, int], Sequence[int]],
        end: Union[List[int], Tuple[int, int], Sequence[int]], algorithm: str = "A*"
) -> List[Tuple[int, int]]:
    """
    if finds the most efficient path from 1 point to another
    if the value of the grid is 0 then the algorithm can go there if it is something over 0 then the algorithm considers ot a wall
    :param start: the start
    :param end: the goal
    :param grid: List[List[int]]
    :param algorithm: str="A*"
    :return: List[Tuple[int, int]]
    """
    if algorithm.lower() == "a*":
        columns: int = len(grid)
        rows: int = len(grid[0])

        grid: List[List[ASPos]] = [[ASPos((i, j), grid[i][j]) for j in range(rows)] for i in range(columns)]

        start: ASPos = grid[start[0]][start[1]]
        end: ASPos = grid[end[0]][end[1]]

        count: int = 0
        open_set: PriorityQueue = PriorityQueue()
        open_set.put((0, count, start))

        came_from: Dict = dict()

        g_score: Dict[ASPos, float] = {pos: float("inf") for row in grid for pos in row}
        g_score[start] = 0
        f_score: Dict[ASPos, float] = {pos: float("inf") for row in grid for pos in row}
        f_score[start] = _heuristic(start, end)

        open_set_hash: Set[ASPos] = {start}

        while not open_set.empty():  # could be replaced with while open_set.qsize():
            # get the best spot that we have available
            current: ASPos = open_set.get()[2]
            open_set_hash.remove(current)

            if current is end:
                path = []
                while current in came_from:
                    current = came_from[current]
                    path.append(tuple(current[0:2]))
                path.reverse()
                return path

            for neighbor in current.neighbors(grid):  # type: ASPos
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + _heuristic(neighbor, end)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

        return []
    elif algorithm.lower() == "bfs":
        raise Notimplemented("Breath First Search is not implemented yet")
    else:
        raise TypeError(f"unrecognised pathfinding algorithm '{algorithm}'. Possible algorithms: A* and BFS")


__all__ = [
    "load_image",
    "load_alpha_image",
    "resize_smooth_image",
    "resize_image",
    "resize_image_ratio",
    "resizex",
    "left_click",
    "middle_click",
    "right_click",
    "get_font",
    "wrap_multi_lines",
    "blit_multiple_lines",
    "pixel_perfect_collision",
    "get_distance",
    "flatten",
    "get_cloth",
    "clamp",
    "remap",
    "lerp",
    "quadratic_bezier",
    "bezier",
    "get_neighbors",
    "get_neighbors_index",
    "pathfinding"
]
