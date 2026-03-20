"""Configuration module for maze generation.

This module defines the MazeConfig dataclass, which encapsulates all parameters
needed to generate a maze. It handles validation of configuration parameters
including dimensions, entry/exit coordinates, perfection flag, and optional
random seed for reproducibility.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MazeConfig:
    """
    Configuration for maze generation.

    Attributes:
        width (int): Maze width (number of columns).
        height (int): Maze height (number of rows).
        entry (tuple[int, int]): Entry cell coordinates (x, y).
        exit_ (tuple[int, int]): Exit cell coordinates (x, y).
        perfect (bool): Whether the maze is perfect (no loops, one solution).
        seed (int | None): Optional random seed for reproducibility.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    perfect: bool
    seed: int | None = None

    def __post_init__(self) -> None:
        """Validate all fields after object is created.

        Checks that width and height are valid integers, coordinates are
        properly formatted and in bounds, entry and exit are different,
        and optional seed is an integer.

        Raises:
            ValueError: If any validation check fails.
        """
        # Integers
        if not isinstance(self.width, int) or not isinstance(self.height, int):
            raise ValueError("WIDTH and HEIGHT must be integers")
        if self.width < 2 or self.height < 2:
            raise ValueError("WIDTH and HEIGHT must be at least 2")

        # Coordinates format
        for name, coords in [("ENTRY", self.entry), ("EXIT", self.exit_)]:
            if not isinstance(coords, tuple) or len(coords) != 2:
                raise ValueError(f"{name} must be a tuple of two integers")
            if not all(isinstance(v, int) for v in coords):
                raise ValueError(f"{name} coordinates must be integers")

        # Coordinates bounds
        for name, (x, y) in [("ENTRY", self.entry), ("EXIT", self.exit_)]:
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(
                    f"{name} ({x},{y}) is out of bounds"
                )

        # Logic
        if self.entry == self.exit_:
            raise ValueError("ENTRY and EXIT must be different cells")

        # Boolean
        if not isinstance(self.perfect, bool):
            raise ValueError("PERFECT must be a boolean")

        # Seed
        if self.seed is not None and not isinstance(self.seed, int):
            raise ValueError("SEED must be an integer")
