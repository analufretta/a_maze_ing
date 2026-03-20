"""Depth-first search algorithm for perfect maze generation.

This module implements iterative DFS to carve paths through a maze,
creating a perfect maze (connected, no loops) while respecting blocked cells.
"""

import random


def dfs_iterative(
        grid: list[list[int]],
        rows: int,
        cols: int,
        blocked: list[list[bool]]
        ) -> None:
    """Generate maze using iterative DFS, skipping blocked cells.

    Modifies the grid in place by removing walls between visited cells,
    creating a spanning tree that connects all unblocked cells. Blocked
    cells are treated as already visited.

    Args:
        grid: 2D list of integers with wall bitmasks (modified in place).
              Bit flags: 1=north, 2=east, 4=south, 8=west walls.
        rows: Number of rows in the grid.
        cols: Number of columns in the grid.
        blocked: 2D list of booleans indicating which cells are blocked.
    """
    visited: list[list[bool]] = [[False] * cols for _ in range(rows)]

    # Mark blocked cells as already visited so DFS ignores them
    for r in range(rows):
        for c in range(cols):
            if blocked[r][c]:
                visited[r][c] = True

    start_row, start_col = random.randrange(rows), random.randrange(cols)
    while blocked[start_row][start_col]:
        start_row, start_col = random.randrange(rows), random.randrange(cols)

    stack = [(start_row, start_col)]
    visited[start_row][start_col] = True

    while stack:
        # Select the last vertice in stack
        row, col = stack[-1]

        neighbours = def_neighbours(row, col, rows, cols)
        unvisited = [(r, c) for r, c in neighbours if not visited[r][c]]

        if unvisited:
            r, c = random.choice(unvisited)
            # Remove vertice walls depending on the direction you go
            if r == row and c > col:  # East
                grid[row][col] &= ~2
                grid[r][c] &= ~8
            elif r == row and c < col:  # West
                grid[row][col] &= ~8
                grid[r][c] &= ~2
            elif c == col and r > row:  # South
                grid[row][col] &= ~4
                grid[r][c] &= ~1
            elif c == col and r < row:  # North
                grid[row][col] &= ~1
                grid[r][c] &= ~4
            visited[r][c] = True
            stack.append((r, c))
        else:
            stack.pop()


def def_neighbours(cur_row: int, cur_col: int,
                   rows: int, cols: int) -> list[tuple[int, int]]:
    """Get valid neighbors in all four cardinal directions.

    Returns all neighboring cells that exist within grid bounds, checking
    north, south, west, and east relative to the current position.

    Args:
        cur_row: Current row coordinate.
        cur_col: Current column coordinate.
        rows: Total number of rows in the grid.
        cols: Total number of columns in the grid.

    Returns:
        List of valid neighbor coordinates as (row, col) tuples.
    """
    north = cur_row - 1
    south = cur_row + 1
    west = cur_col - 1
    east = cur_col + 1

    neighbours = []
    if north >= 0:
        neighbours.append((north, cur_col))
    if south < rows:
        neighbours.append((south, cur_col))
    if west >= 0:
        neighbours.append((cur_row, west))
    if east < cols:
        neighbours.append((cur_row, east))

    return neighbours
