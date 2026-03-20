"""Utilities for checking 3x3 area constraints in maze generation.

This module prevents the creation of excessively large open areas
(3x3 blocks) when removing walls in imperfect maze generation.
"""


def would_create_3x3(grid: list[list[int]],
                     r: int, c: int, direction: str) -> bool:
    """Check if removing a wall would create a 3x3 open area.

    Examines all 2x2 overlapping 3x3 blocks around the specified cell
    to determine if removing a wall in the given direction would create
    a forbidden 3x3 open area.

    Args:
        grid: 2D list of integers representing maze cells with wall bitmasks.
        r: Row coordinate of the cell.
        c: Column coordinate of the cell.
        direction: Direction of wall to remove ("east" or "south").

    Returns:
        True if removing the wall would create a 3x3 open area,
        False otherwise.
    """
    skip_wall = (r, c, direction)

    for top in range(r - 1, r + 1):
        for left in range(c - 1, c + 1):
            if top < 0 or left < 0:
                continue
            if top + 2 >= len(grid) or left + 2 >= len(grid[0]):
                continue
            if is_3x3_open(grid, top, left, skip_wall):
                return True
    return False


def is_3x3_open(grid: list[list[int]], r: int, c: int,
                skip_wall: tuple[int, int, str]) -> bool:
    """Check if the 3x3 block starting at (r,c) is fully open.

    Verifies that a 3x3 area has no south walls in the top 2 rows and
    no east walls in the left 2 columns, allowing for an optional wall
    to be excluded from the check (the wall being removed).

    Args:
        grid: 2D list of integers representing maze cells with wall bitmasks.
              Bit flags: 4=south wall, 2=east wall.
        r: Row coordinate where the 3x3 block starts.
        c: Column coordinate where the 3x3 block starts.
        skip_wall: Tuple of (row, col, direction) for the wall being excluded
                   from the openness check.

    Returns:
        True if the 3x3 block is fully open (except for skip_wall),
        False otherwise.
    """
    skip_r, skip_c, direction = skip_wall
    # Check no south walls in top 2 rows
    for row in range(r, r + 2):
        for col in range(c, c + 3):
            if row == skip_r and col == skip_c and direction == "south":
                continue
            if grid[row][col] & 4 == 4:  # south wall exists
                return False
    # Check no east walls in left 2 cols
    for row in range(r, r + 3):
        for col in range(c, c + 2):
            if row == skip_r and col == skip_c and direction == "east":
                continue
            if grid[row][col] & 2 == 2:  # east wall exists
                return False
    return True
