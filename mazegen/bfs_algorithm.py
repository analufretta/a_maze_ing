"""Breadth-first search algorithm for solving mazes.

This module provides pathfinding functionality using BFS to find
the shortest path through a maze from entry to exit.
"""

from collections import deque


def bfs(
        grid: list[list[int]],
        start: tuple[int, int],
        exit_: tuple[int, int],
        ) -> list[tuple[int, int]]:
    """Find shortest path through maze using breadth-first search.

    Args:
        grid: 2D list of integers representing maze cells with wall bitmasks.
        start: Starting cell coordinates as (row, col).
        exit_: Exit cell coordinates as (row, col).

    Returns:
        List of coordinates representing the path from start to exit.
    """
    queue = deque([start])
    trace: dict[tuple[int, int], tuple[int, int] | None] = {start: None}

    while queue:
        current: tuple[int, int] = queue.popleft()
        if current == exit_:
            break
        for neighbor in get_open_neighbors(grid, current):
            if neighbor not in trace:
                trace[neighbor] = current
                queue.append(neighbor)

    path = [exit_]
    one_before = trace[exit_]
    while one_before is not None:
        path.append(one_before)
        one_before = trace[one_before]
    path.reverse()
    return path


def get_open_neighbors(grid: list[list[int]],
                       current: tuple[int, int]) -> list[tuple[int, int]]:
    """Get all neighboring cells with open walls (traversable directions).

    Checks all four cardinal directions (north, south, west, east) and
    returns neighbors that have open walls in the current cell.

    Args:
        grid: 2D list of integers representing maze cells with wall bitmasks.
              Bit flags: 1=north, 2=east, 4=south, 8=west.
        current: Current cell coordinates as (row, col).

    Returns:
        List of neighbor coordinates (row, col) that are accessible.
    """
    neighbors = []
    r, c = current
    rows = len(grid)
    cols = len(grid[0])

    # establidh directions
    n, s, w, e = r - 1, r + 1, c - 1, c + 1

    # check if directions have open walls
    if n >= 0 and not grid[r][c] & 1:
        neighbors.append((n, c))
    if s < rows and not grid[r][c] & 4:
        neighbors.append((s, c))
    if w >= 0 and not grid[r][c] & 8:
        neighbors.append((r, w))
    if e < cols and not grid[r][c] & 2:
        neighbors.append((r, e))
    return neighbors
