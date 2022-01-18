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
pathfinding from 1 point to another
"""

from typing import List, Tuple, Generator, Union, Dict, Sequence, Set

import queue


Number = Union[int, float]


class _ASPos:  # it is used for A* pathfinding
    __slots__ = "i", "j", "v", "tp"

    def __init__(self, idxs: Tuple[int, int], v: Number) -> None:
        self.i: int = idxs[0]
        self.j: int = idxs[1]
        self.v: Number = v
        self.tp: Tuple[int, int] = (self.i, self.j)

    def neighbors(self, grid: List[List["_ASPos"]]) -> Generator:
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

    def __repr__(self) -> str:
        return repr(f"${self.i} ${self.j} ${self.v}")


def AS_heuristic(p1: _ASPos, p2: _ASPos) -> Number:  # it is used for A* pathfinding
    return int(abs(p1.i - p2.i) + abs(p1.j - p2.j))


def pathfinding(
    grid: List[List[int]],
    start: Union[List[int], Tuple[int, int], Sequence[int]],
    end: Union[List[int], Tuple[int, int], Sequence[int]],
) -> Sequence[Tuple[float, float]]:
    """
    if finds the most efficient path from one point to another
    if the value of the grid is 0 then the algorithm can go there if it is something over 0 then the algorithm considers ot a wall
    :param start: Sequence[int]
    :param end: Sequence[int]
    :param grid: List[List[int]]
    :return: List[Tuple[int, int]]
    """
    ASPGrid: List[List[_ASPos]] = [
        [_ASPos((i, j), grid[i][j]) for j in range(len(grid[0]))]
        for i in range(len(grid))
    ]

    ASPstart: _ASPos = ASPGrid[start[0]][start[1]]
    ASPend: _ASPos = ASPGrid[end[0]][end[1]]

    count: int = 0
    open_set: queue.PriorityQueue = queue.PriorityQueue()
    open_set.put((0, count, ASPstart))
    open_set_hash: Set[_ASPos] = {ASPstart}

    came_from: Dict = {}

    g_score: Dict[_ASPos, float] = {pos: float("inf") for row in ASPGrid for pos in row}
    g_score[ASPstart] = 0
    f_score: Dict[_ASPos, float] = {pos: float("inf") for row in ASPGrid for pos in row}
    f_score[ASPstart] = AS_heuristic(ASPstart, ASPend)

    current: _ASPos
    while not open_set.empty():  # could be replaced with while open_set.qsize():
        # get the best spot that we have available
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current is ASPend:
            path = []
            while current in came_from:
                current = came_from[current]
                path.append(current.tp)
            path.reverse()
            return path

        for neighbor in current.neighbors(ASPGrid):  # type: _ASPos
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + AS_heuristic(neighbor, ASPend)
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

    return []


__all__ = ["pathfinding"]
