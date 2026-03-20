# mazegen Package Documentation

`mazegen` is a reusable Python package for generating and solving mazes.

It exposes two public objects:
- `MazeConfig`
- `MazeGenerator`

## Public API

```python
from mazegen import MazeConfig, MazeGenerator
```

## Quick Start

```python
from mazegen import MazeConfig, MazeGenerator

config = MazeConfig(
    width=25,
    height=25,
    entry=(0, 0),
    exit_=(24, 24),
    perfect=True,
    seed=42,
)

maze = MazeGenerator(config)

grid = maze.get_grid()
entry = maze.get_entry()                     # (x, y)
exit_ = maze.get_exit()                      # (x, y)
solution_coords = maze.get_solution_coord()  # [(row, col), ...]
solution_dirs = maze.get_solution_dir()      # "N", "E", "S", "W" sequence
```

## Coordinate Conventions

The package intentionally uses two coordinate conventions depending on context:

- Entry/exit configuration and getters use `(x, y)`.
- Solved path coordinates use `(row, col)`.

This mirrors the grid representation (`grid[row][col]`) while keeping entry/exit user-facing coordinates intuitive.

## `MazeConfig`

`MazeConfig` is an immutable dataclass (`frozen=True`) used to validate all generation parameters.

### Signature

```python
MazeConfig(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    perfect: bool,
    seed: int | None = None,
)
```

### Validation Rules

- `width` and `height` must be integers and at least `2`.
- `entry` and `exit_` must be tuples of exactly two integers.
- Entry/exit must be in bounds:
  - `0 <= x < width`
  - `0 <= y < height`
- `entry` and `exit_` must be different.
- `perfect` must be a boolean.
- `seed`, when provided, must be an integer.

Invalid values raise `ValueError`.

## `MazeGenerator`

`MazeGenerator` builds the maze immediately at instantiation time.

### Signature

```python
MazeGenerator(config: MazeConfig)
```

### Internal Generation Pipeline

1. Create a fully closed grid (`0b1111` in each cell).
2. Seed RNG if `config.seed` is set.
3. Block center cells to draw a "42" pattern when dimensions are at least `7x9`.
4. Generate a perfect maze using iterative DFS.
5. If `perfect=False`, remove a small subset of internal walls to create loops.
6. Solve shortest path with BFS.
7. Convert solved coordinates into direction string.

## Methods

### `get_grid() -> list[list[int]]`
Returns the maze grid where each cell stores wall bits:

- `1`: north wall
- `2`: east wall
- `4`: south wall
- `8`: west wall

A set bit means the wall is closed.

### `get_solution_coord() -> list[tuple[int, int]]`
Returns shortest path as `(row, col)` coordinates.

### `get_solution_dir() -> str`
Returns shortest path as direction characters (`N`, `S`, `W`, `E`).

### `get_entry() -> tuple[int, int]`
Returns entry point as `(x, y)`.

### `get_exit() -> tuple[int, int]`
Returns exit point as `(x, y)`.

## Perfect vs Imperfect Mazes

- `perfect=True`: DFS spanning-tree maze (single path between reachable cells).
- `perfect=False`: Additional wall removals add loops.

For imperfect mazes, the package includes a guard to avoid creating fully open 3x3 areas when removing walls.

## "42" Pattern Behavior

- If maze size is at least `7x9`, a centered blocked-cell pattern forms the text "42".
- If maze is smaller, generation proceeds without this pattern and prints a warning.
- If entry or exit overlaps a blocked "42" cell, generation raises `ValueError`.

## Example: Minimal Script

```python
from mazegen import MazeConfig, MazeGenerator

cfg = MazeConfig(
    width=10,
    height=8,
    entry=(0, 0),
    exit_=(9, 7),
    perfect=False,
)

mz = MazeGenerator(cfg)

print("Entry:", mz.get_entry())
print("Exit:", mz.get_exit())
print("Path:", mz.get_solution_dir())
for row in mz.get_grid():
    print("".join(format(cell, "X") for cell in row))
```

## Package Layout

- `__init__.py`: public exports
- `mazeconfig.py`: config dataclass and validation
- `mazegen.py`: `MazeGenerator` implementation
- `dfs_algorithm.py`: DFS generation
- `bfs_algorithm.py`: BFS shortest-path solving
- `imperfect_maze.py`: wall removal for imperfect mazes
- `check_3x3.py`: safety check for imperfect wall removal

## Version

Current packaged wheel in repository root:
- `mazegen-1.0.0-py3-none-any.whl`
