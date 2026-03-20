*This project has been created as part of the 42 curriculum by \<afretta\>, \<leodum\>.*

# A-Maze-Ing

> Python maze generator and interactive terminal renderer for the 42 `a-maze-ing` project.

---

## Description

A-Maze-Ing is a Python maze generator and visualizer. The program reads a configuration file, generates a valid maze (optionally perfect — with a single path between entry and exit), and writes the result to a file using a hexadecimal wall encoding. The maze is displayed interactively in the terminal using a curses-based ASCII renderer, and always contains a hidden "42" pattern formed by fully-closed cells.

This project:
- Parses and validates a configuration file.
- Generates a maze using iterative DFS (perfect by default).
- Optionally makes it imperfect by removing a small number of walls.
- Embeds a "42" pattern in the maze when dimensions allow it.
- Solves the maze with BFS and stores the shortest path.
- Displays the maze in an interactive curses terminal UI.
- Provides color management, animated path display, and a solve-it-yourself game mode.
- Writes the maze, entry/exit coordinates, and shortest path to an output file.

### Project Structure

```
a_maze_ing.py          # Entry point
file_config.py         # Config parser + validation
render.py              # Main curses rendering loop and display logic
additional_render.py   # Color manager and manual solve game mode
make_output_file.py    # Maze export writer
mazegen/               # Reusable maze generation package
config.txt             # Default runtime configuration
Makefile               # Common commands (run, lint, clean, etc.)
```

---

## Instructions

### Requirements

- Python 3.10+
- `pip`

Install dependencies:

```bash
make install
```

### Run

```bash
python3 a_maze_ing.py config.txt
```

Or:

```bash
make run
```

Debug mode:

```bash
make debug
```

### Makefile Commands

```bash
make help          # Show command list
make install       # Install dependencies from requirements.txt
make run           # Run with config.txt
make debug         # Run in pdb
make check         # Quick import checks
make lint          # flake8 + mypy (configured flags)
make lint-strict   # flake8 + mypy --strict
make clean         # Remove __pycache__, .mypy_cache, *.pyc
make distclean     # clean + remove configured output file
```

---

## Configuration File

Expected format: one `KEY=VALUE` per line. Lines starting with `#` are ignored.

**Required keys:**

| Key | Type | Description | Example |
|---|---|---|---|
| `WIDTH` | int (>= 2) | Maze width in cells | `WIDTH=25` |
| `HEIGHT` | int (>= 2) | Maze height in cells | `HEIGHT=25` |
| `ENTRY` | `x,y` | Entry coordinates | `ENTRY=0,0` |
| `EXIT` | `x,y` | Exit coordinates | `EXIT=24,24` |
| `OUTPUT_FILE` | filename | Output filename (no `/` or `\\`) | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True`/`False` | Whether maze is perfect | `PERFECT=True` |

**Optional key:**

| Key | Type | Description | Example |
|---|---|---|---|
| `SEED` | int | Seed for reproducibility | `SEED=42` |

Example `config.txt`:

```ini
# Default configuration
WIDTH=25
HEIGHT=25
ENTRY=0,0
EXIT=24,24
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

**Validation rules:**
- Entry and exit must be inside maze bounds.
- Entry and exit must be different cells.
- Output must be a filename, not a path.

---

## Output File Format

The output file contains:

1. Maze grid in hex, one row per line — one hex digit per cell
2. One empty line
3. Entry coordinates as `x,y`
4. Exit coordinates as `x,y`
5. Shortest path as space-separated directions (`N`, `E`, `S`, `W`)

Each cell is one hex digit encoding wall bit flags:

| Bit | Value | Direction |
|---|---|---|
| 0 | 1 | North wall |
| 1 | 2 | East wall |
| 2 | 4 | South wall |
| 3 | 8 | West wall |

A set bit means the wall is closed.

Example:
```
9a5c3f
3f6291
...

0,0
24,24
S S E E N E S W S
```

---

## Interactive Display

Once the maze is displayed, the following keys are available:

| Key | Action |
|---|---|
| `1` | Regenerate a new maze |
| `2` | Show / Hide the animated solution path |
| `3` | Cycle through wall color presets |
| `4` | Open the color manager |
| `5` | Play solve-it-yourself mode |
| `6` | Quit |

### Path Animation
Pressing `2` animates the solution path cell by cell. Press any key during animation to skip and display the full path instantly.

### Color Manager
Press `4` to enter the color manager. Select which element to recolor (walls, path, "42" pattern, entry/exit), then choose from 7 available colors displayed as colored swatches. Colors persist across maze regenerations.

### Solve It Yourself
Press `5` to enter game mode. Navigate using arrow keys. The player is blocked by walls — hitting a wall ends the game. Reach the exit to win.

---

## Algorithms

### Generation — Iterative DFS (`mazegen/dfs_algorithm.py`)
The maze is generated using an iterative depth-first search (randomized DFS), also known as the recursive backtracker algorithm. Starting from the entry cell, the algorithm visits unvisited neighbors in random order, carving passages until all cells have been visited, producing a perfect maze (spanning tree).

**Why DFS?**
- Simple to implement and reason about
- Produces long, winding corridors with few dead ends — visually interesting mazes
- Naturally produces a perfect maze without extra connectivity checks
- Efficient — runs in O(n) time and space

### Imperfect Maze — Wall Removal (`mazegen/imperfect_maze.py`)
When `PERFECT=False`, a controlled number of walls are removed after generation. A 3×3 open-area guard (`mazegen/check_3x3.py`) ensures no area larger than 2×2 cells is fully open.

### Solving — BFS (`mazegen/bfs_algorithm.py`)
The shortest path from entry to exit is computed using breadth-first search on the maze graph, where edges exist between cells with no wall between them.

### "42" Pattern
When maze dimensions are at least 7×9, a centered set of fully-closed cells (`0xF`) shaped as "42" is embedded before generation. The DFS carves around these locked cells. If the maze is too small, generation continues without the pattern and a warning is printed. Entry/exit overlapping "42" cells raises a `ValueError`.

---

## Reusable Components

The maze generation logic is fully decoupled from the display layer.

### `mazegen` Package

Exposes `MazeConfig` and `MazeGenerator`:

```python
from mazegen import MazeConfig, MazeGenerator

cfg = MazeConfig(
    width=25,
    height=25,
    entry=(0, 0),
    exit_=(24, 24),
    perfect=True,
    seed=42,
)

maze = MazeGenerator(cfg)

grid = maze.get_grid()                   # 2D list of wall bitmasks
entry = maze.get_entry()                 # (row, col)
exit_ = maze.get_exit()                  # (row, col)
path_coords = maze.get_solution_coord()  # list of (row, col)
path_dirs = maze.get_solution_dir()      # list of 'N', 'E', 'S', 'W'
```

### Build Wheel

`pyproject.toml` is configured with Hatchling. The repository includes `mazegen-1.0.0-py3-none-any.whl`.

```bash
python -m build
```

### `render.py`

The rendering module is independent of generation logic. It accepts any valid 2D list of wall bitmasks and a state dictionary. Key reusable components:

- `display_maze(stdscr, state)` — renders any valid maze grid with walls, entry, exit, and optional path
- `get_maze_offsets(stdscr, state)` — computes centered offsets for any maze size and terminal size
- `draw_path(stdscr, state)` — animates a solution path given as a list of `(row, col)` coordinates
- `write_output_file(state, filename)` — serializes maze to the hex format

---

## Technical Choices

### Terminal Rendering with `curses`
Python's built-in `curses` library was chosen for the graphical display. Since the project is written in Python and `curses` is part of the standard library, it requires no additional installation and is fully cross-platform on Unix systems. It satisfies the "terminal ASCII rendering" requirement while providing full color support and precise cursor positioning.

### Wall Encoding with Bitmasks
Each cell's walls are encoded as a 4-bit integer where each bit represents one cardinal direction. This makes wall queries a single bitwise AND operation and maps directly to the hex output format required by the spec.

### Corner-Based Rendering
The maze is rendered by iterating over a `(rows+1) × (cols+1)` grid of corner intersection points. At each corner, the surrounding cells are checked for walls and the result maps to a Unicode box-drawing character (`┼`, `├`, `┐`, etc.). This produces clean connected wall lines rather than disconnected segments.

### State Dictionary Pattern
All display state (maze data, colors, path visibility, player position) is stored in a single dictionary passed between functions. This avoids global variables and makes the full display state explicit — particularly useful for regeneration and color management that need to modify multiple aspects of the display at once.

---

## Resources

### Maze Generation
- [Maze Generation Algorithms — YouTube](https://www.youtube.com/watch?v=ioUl1M77hww)
- [DFS — Depth First Search — YouTube](https://www.youtube.com/watch?v=PMMc4VsIacU)
- [Graph Theory Basics — YouTube](https://www.youtube.com/watch?v=LFKZLXVO-Dg)
- [Shortest Path Algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze-solving_algorithm#Shortest_path_algorithm)
- [Jamis Buck's maze algorithm blog series](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- [Think Labyrinth — comprehensive maze reference](http://www.astrolog.org/labyrnth/algrithm.htm)

### Terminal Rendering
- [Python official curses how-to](https://docs.python.org/3/howto/curses.html)
- [DevDungeon curses tutorial](https://www.devdungeon.com/content/curses-programming-python)
- [Wasim Lorgat — build a text editor with curses](https://wasimlorgat.com/posts/editor.html)
- [Box-drawing characters — Wikipedia](https://en.wikipedia.org/wiki/Box-drawing_character)

### Python
- [Python `random` module documentation](https://docs.python.org/3/library/random.html)
- [Python Packaging User Guide](https://packaging.python.org/en/latest/)
- [mypy documentation](https://mypy.readthedocs.io/en/stable/)

### AI Usage

Claude (Anthropic) was used throughout this project as a learning and debugging assistant.

**Maze generation side:**
- Suggesting initial project structure and module interface design
- Helping debug generation and validation logic
- Drafting docstring templates for functions
- Explaining bitmasking conventions for the hex output format

**Rendering side:**
- Guidance on corner-based rendering approach and curses coordinate system
- Explaining the event loop pattern and state management architecture
- Explaining Unicode box-drawing characters and how to build a lookup table

All suggestions were reviewed, tested, and understood by both team members before being included in the project.

---

## Team & Project Management

### Roles

| Member | Responsibilities |
|---|---|
| leodum | Terminal rendering (`render.py`, `additional_render.py`), interactive display, color management, game mode, output file writer |
| afretta | Maze generation (`mazegen/`), BFS pathfinding, config parser, "42" pattern embedding, wall validity, project packaging |

### Planning
- Weekly meeting to discuss progress
- Clear milestones defined
- Re-evaluation of the workload when needed to adapt as necessary


### What Worked Well
- Clear separation between generation and display from the start — both team members could work independently with minimal blocking
- Defining the `MazeGenerator` API early (`.get_grid()`, `.get_entry()`, `.get_solution_coord()`) so both sides could develop in parallel without waiting on each other
- Weekly sync meetings to align on interfaces, data formats, and integration points

### What Could Be Improved

- Adding additional algorithms to create the maze to have different patterns available
- Improving the solving yourself game with scores, reward system, backtracking...etc.
- Code clarity and efficiency improvement

### Tools Used
- **Git / GitHub** — version control and collaboration
- **Claude (Anthropic)** — AI assistant for learning, debugging, and concept explanation
- **Python 3** — primary language
- **flake8 + mypy** — linting and type checking
- **Hatchling** — Python packaging
