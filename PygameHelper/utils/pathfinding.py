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

from typing import List, Tuple, Generator, Union, Dict, Sequence, Set, TypeVar, overload as TpOverload

import queue


Number = Union[int, float]
NeighborOutputType = TypeVar("NeighborOutputType")


class _ASPos:  # it is used for A* pathfinding
    __slots__ = "i", "j", "v"

    def __init__(self, idxs: Tuple[int, int], v: Number) -> None:
        self.i: int = idxs[0]
        self.j: int = idxs[1]
        self.v: Number = v

    @property
    def pos(self) -> Tuple[int, int]:
        return self.i, self.j

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

    @TpOverload
    def __getitem__(self, idx: int) -> int: ...

    @TpOverload
    def __getitem__(self, idx: slice) -> List[int]: ...

    def __getitem__(self, idx: slice) -> Union[int, List[int]]:
        return [self.i, self.j, self.v][idx]

    def __repr__(self) -> str:
        return repr(f"${self.i} ${self.j} ${self.v}")


def AS_heuristic(p1: _ASPos, p2: _ASPos) -> int:  # it is used for A* pathfinding
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def bfs_found_end(path: str, start: Tuple[int, int], end: Tuple[int, int]) -> bool:
    i: int = start[0]
    j: int = start[1]
    for move in path:
        if move in "LR": j += bfs_values[move]
        else: i += bfs_values[move]

    if (i, j) == end:
        return True
    return False


def bfs_valid(grid: List[List[int]], path: str, start: Tuple[int, int]) -> bool:
    i: int = start[0]
    j: int = start[1]
    for move in path:
        if move in "LR": j += bfs_values[move]
        else: i += bfs_values[move]
        if not(0 <= i < len(grid) and 0 <= j < len(grid[0])):
            return False
        elif grid[i][j] != 0:
            return False
    return True


bfs_opposites: Dict[str, str] = {"L": "R", "R": "L", "U": "D", "D": "U", "": "werg"}
bfs_values: Dict[str, int] = {"L": -1, "R": 1, "U": -1, "D": 1, "": 0}


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

        grid: List[List[_ASPos]] = [[_ASPos((i, j), grid[i][j]) for j in range(rows)] for i in range(columns)]

        start: _ASPos = grid[start[0]][start[1]]
        end: _ASPos = grid[end[0]][end[1]]

        count: int = 0
        open_set: queue.PriorityQueue = queue.PriorityQueue()
        open_set.put((0, count, start))

        came_from: Dict = dict()

        g_score: Dict[_ASPos, float] = {pos: float("inf") for row in grid for pos in row}
        g_score[start] = 0
        f_score: Dict[_ASPos, float] = {pos: float("inf") for row in grid for pos in row}
        f_score[start] = AS_heuristic(start, end)

        open_set_hash: Set[_ASPos] = {start}

        while not open_set.empty():  # could be replaced with while open_set.qsize():
            # get the best spot that we have available
            current: _ASPos = open_set.get()[2]
            open_set_hash.remove(current)

            if current is end:
                path = []
                while current in came_from:
                    current = came_from[current]
                    path.append(tuple(current[0:2]))
                path.reverse()
                return path

            for neighbor in current.neighbors(grid):  # type: _ASPos
                temp_g_score = g_score[current] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + AS_heuristic(neighbor, end)
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)

        return []
    elif algorithm.lower() == "bfs":
        moves: List[str] = [""]
        current: str = ""

        start: Tuple[int, int] = tuple(start)
        end: Tuple[int, int] = tuple(end)

        while not bfs_found_end(current, start, end):
            current: str = moves.pop(0)
            for j in ["L", "R", "U", "D"]:
                if not bfs_opposites[current[len(current)-1:]] == j: to_put: str = current + j
                else: to_put = current
                if bfs_valid(grid, to_put, start):
                    moves.append(to_put)

            moves = list(sorted(set(moves), key=moves.index))

        path: List[Tuple[int, int]] = [start]
        for move in current:
            if   move == "L": path.append((path[~0][0], path[~0][1] - 1))
            elif move == "R": path.append((path[~0][0], path[~0][1] + 1))
            elif move == "U": path.append((path[~0][0] - 1, path[~0][1]))
            elif move == "D": path.append((path[~0][0] + 1, path[~0][1]))
        return path[1:]
    else:
        raise TypeError(f"unrecognised pathfinding algorithm '{algorithm}'. Possible algorithms: A* and BFS")


__all__ = ["pathfinding"]
