
"""Maze generation engine.

This module provides the main MazeGenerator class that coordinates
all aspects of maze creation from configuration through solving.
"""

import random

from .mazeconfig import MazeConfig
from .dfs_algorithm import dfs_iterative
from .imperfect_maze import remove_walls
from .bfs_algorithm import bfs


class MazeGenerator:
    """Generator for perfect and imperfect mazes with solutions.

    Creates mazes based on configuration, optionally includes a "42" pattern,
    and solves the maze to provide the solution path.

    Attributes:
        _config: MazeConfig object with maze parameters.
        _grid: 2D list of integers representing the maze structure.
        _pattern: 2D list of booleans indicating blocked cells.
        _coordinates: List of cell coordinates forming the solution path.
        _directions: String of direction characters (N/S/E/W) for the solution.
    """

    def __init__(self, config: MazeConfig) -> None:
        """Initialize and generate a maze.

        Args:
            config: MazeConfig object specifying maze parameters.
        """
        # Genral configuration
        self._config: MazeConfig = config

        # Initialize grid with closed walls
        self._grid: list[list[int]] = self._init_grid(config.height,
                                                      config.width)

        # Generate seed
        if config.seed is not None:
            random.seed(config.seed)

        # Block 42 cells if grid is big enough
        self._pattern: list[list[bool]] = self._block_42grid_cells()

        # Generate maze modifying self._grid
        self._perfect_maze_gen()

        # Remove walls in self._grid if perfect = False
        if not self._config.perfect:
            self._extra_paths_gen()

        # Solve maze
        self._coordinates: list[tuple[int, int]] = self._solve_maze()
        self._directions: str = self._make_directions()

    @staticmethod
    def _init_grid(rows: int, cols: int) -> list[list[int]]:
        """Initialize grid with all walls closed.

        Creates a grid where each cell has value 15 (0b1111), representing
        all four walls (north, east, south, west) closed.

        Args:
            rows: Number of rows in the grid.
            cols: Number of columns in the grid.

        Returns:
            2D list of integers where each cell is initialized to 15.
        """
        return [[15] * cols for _ in range(rows)]

    def _block_42grid_cells(self) -> list[list[bool]]:
        """Build and block the "42" pattern in the center of the grid.

        Creates a pattern spelling "42" in the maze if the grid is large enough
        (at least 7 rows and 9 columns).
        Prints a warning if the grid is too small.

        Returns:
            2D list of booleans indicating which cells are blocked.

        Raises:
            ValueError: If entry/exit coordinates overlap with the 42 pattern.
        """
        rows = self._config.height
        cols = self._config.width

        blocked: list[list[bool]] = [[False] * cols for _ in range(rows)]

        if rows >= 7 and cols >= 9:
            r = (rows // 2) - 2
            c = (cols // 2) - 3

            coord_42 = [(r, c), (r+1, c), (r+2, c), (r+2, c+1),
                        (r+2, c+2), (r+3, c+2), (r+4, c+2), (r, c+4),
                        (r, c+5), (r, c+6), (r+1, c+6), (r+2, c+6),
                        (r+2, c+5), (r+2, c+4), (r+3, c+4), (r+4, c+4),
                        (r+4, c+5), (r+4, c+6)]
            for row, col in coord_42:
                blocked[row][col] = True
        else:
            print("Warning: "
                  "maze is too small to include '42' pattern, omitting it.")

        ecol, erow = self._config.entry
        xcol, xrow = self._config.exit_
        if blocked[erow][ecol] or blocked[xrow][xcol]:
            raise ValueError("entry or exit coordinates "
                             "overlap with '42' pattern.")

        return blocked

    def _perfect_maze_gen(self) -> None:
        """Generate a perfect maze using depth-first search.

        Modifies self._grid in place using the DFS algorithm to create
        a maze where every cell is reachable and there is exactly one path
        between any two cells.
        """
        dfs_iterative(self._grid, self._config.height,
                      self._config.width, self._pattern)

    def _extra_paths_gen(self) -> None:
        """Create extra paths in the maze for imperfect mazes.

        Removes walls from the perfect maze to create loops and multiple
        paths between cells, making the maze imperfect.
        """
        remove_walls(self._grid, self._config.width,
                     self._config.height, self._pattern)

    def _solve_maze(self) -> list[tuple[int, int]]:
        """Solve the maze using breadth-first search.

        Finds the shortest path from entry to exit using BFS and
        converts from (row, col) format to the internal coordinate system.

        Returns:
            List of coordinates (row, col) representing the solution path.
        """
        entry_col, entry_row = self._config.entry
        exit_col, exit_row = self._config.exit_
        path = bfs(self._grid, (entry_row, entry_col), (exit_row, exit_col))
        # path given is (row,col), whcih means (y,x)
        return path

    def _make_directions(self) -> str:
        """Convert solution path to direction string.

        Analyzes the solution coordinate path and generates a
        string of direction characters (N/S/E/W) representing
        the moves from entry to exit.

        Returns:
            String of direction characters (N, S, W, E) for the solution.
        """
        path: list[tuple[int, int]] = self._coordinates

        directions: str = ''

        for i in range(len(path) - 1):
            row1, col1 = path[i]
            row2, col2 = path[i + 1]
            if row2 == row1 - 1:
                directions += 'N'
            elif row2 == row1 + 1:
                directions += 'S'
            elif col2 == col1 - 1:
                directions += 'W'
            elif col2 == col1 + 1:
                directions += 'E'
        return directions

    def get_grid(self) -> list[list[int]]:
        """Return the maze grid.

        Returns:
            2D list of integers where each value is a bitmask representing
            wall configuration: 1=north, 2=east, 4=south, 8=west.
        """
        return self._grid

    def get_solution_coord(self) -> list[tuple[int, int]]:
        """Return the solution path as coordinates.

        Returns:
            List of (row, col) tuples representing the path from entry to exit.
        """
        return self._coordinates

    def get_solution_dir(self) -> str:
        """Return the solution path as direction string.

        Returns:
            String of direction characters (N, S, W, E) from entry to exit.
        """
        return self._directions

    def get_entry(self) -> tuple[int, int]:
        """Return entry point coordinates.

        Returns:
            Tuple of (x, y) coordinates for the maze entry.
        """
        return tuple(self._config.entry)  # type: ignore

    def get_exit(self) -> tuple[int, int]:
        """Return exit point coordinates.

        Returns:
            Tuple of (x, y) coordinates for the maze exit.
        """
        return tuple(self._config.exit_)  # type: ignore
