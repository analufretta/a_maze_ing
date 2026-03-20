
def write_output_file(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: str,
    output_path: str
) -> None:
    """Write maze to output file in the required format.

    Format:
        - One hex digit per cell, rows on separate lines
        - Empty line
        - Entry as "col,row" (x,y)
        - Exit as "col,row" (x,y)
        - Shortest path as string of "NESW"

    Args:
        grid: 2D list of wall values (row-major: grid[row][col]).
        entry: (row, col) of entry cell.
        exit_: (row, col) of exit cell.
        path: str of maze solution
        output_path: Path to the output file.

    Raises:
        IOError: If the file cannot be written.
        ValueError: If no path exists between entry and exit.
    """

    try:
        with open(output_path, 'w') as f:
            # Write hex grid row by row
            for row in grid:
                f.write("".join(format(cell, 'X') for cell in row) + "\n")

            # Empty line separator
            f.write("\n")

            entry_x, entry_y = entry
            exit_x, exit_y = exit_

            # Entry, exit, path  —  coordinates are col,row per the subject
            f.write(f"{entry_x},{entry_y}\n")
            f.write(f"{exit_x},{exit_y}\n")
            f.write(f"{path}\n")

    except IOError as e:
        raise IOError(f"Failed to write output file '{output_path}': {e}")
