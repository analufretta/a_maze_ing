"""Imperfect maze generation by removing walls.

This module adds extra paths to a perfect maze by selectively removing
internal walls while preventing the creation of excessively large open areas.
"""

import random
from .check_3x3 import would_create_3x3


def remove_walls(
        grid: list[list[int]],
        width: int,
        height: int,
        blocked: list[list[bool]]
        ) -> None:
    """Remove walls to create extra paths (imperfect maze).

    Randomly removes approximately 5% of closed internal walls to add
    loops to the maze, while preventing 3x3 open areas. Modifies grid in place.

    Args:
        grid: 2D list of integers with wall bitmasks (modified in place).
        width: Number of columns in the grid.
        height: Number of rows in the grid.
        blocked: 2D list of booleans indicating blocked cells.
    """

    candidates = closed_internal_walls(grid, width, height, blocked)
    walls_to_remove = int(0.05 * len(candidates))
    if walls_to_remove == 0:
        walls_to_remove = 1
    random.shuffle(candidates)

    counter = 0
    while counter < walls_to_remove and candidates:
        r, c, nr, nc = candidates.pop()
        if r == nr:
            if not would_create_3x3(grid, r, c, "east"):
                grid[r][c] &= ~2
                grid[nr][nc] &= ~8
                counter += 1
        elif c == nc:
            if not would_create_3x3(grid, r, c, "south"):
                grid[r][c] &= ~4
                grid[nr][nc] &= ~1
                counter += 1


def closed_internal_walls(
        grid: list[list[int]],
        width: int,
        height: int,
        blocked: list[list[bool]]
        ) -> list[tuple[int, int, int, int]]:
    """Find all closed internal walls between unblocked cells.

    Scans the grid for walls between adjacent unblocked cells that are
    still closed (candidates for removal to create extra paths).

    Args:
        grid: 2D list of integers with wall bitmasks.
              Bit flags: 2=east wall, 4=south wall.
        width: Number of columns in the grid.
        height: Number of rows in the grid.
        blocked: 2D list of booleans indicating blocked cells.

    Returns:
        List of wall tuples as (r1, c1, r2, c2) where first cell is
        followed by the cell on the other side of the wall.
    """
    candidates = []
    for r in range(height):
        for c in range(width):
            if not blocked[r][c]:
                if (c < width - 1
                        and not blocked[r][c + 1]
                        and grid[r][c] & 2):
                    candidates.append((r, c, r, c + 1))
                if (r < height - 1
                        and not blocked[r + 1][c]
                        and grid[r][c] & 4):
                    candidates.append((r, c, r + 1, c))
    return candidates
