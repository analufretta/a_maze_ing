from dataclasses import dataclass
CELL_HEIGHT = 2
CELL_WIDTH = 4


@dataclass
class State:
    maze: list[list[int]]
    rows: int
    cols: int
    m_color: int
    color_42: int
    p_color: int
    e_color: int
    show_path: bool
    path: list[tuple[int, int]]
    entry: tuple[int, int]
    exit_: tuple[int, int]
    COLORS: list[int]
    player: tuple[int, int]


menu = [
        "=== A-Maze-Ing ===",
        "1. Regenerate",
        "2. Show/Hide path",
        "3. Rotate colors",
        "4. Colors Manager",
        "5. Surprise?",
        "6. Quit",
    ]

corners = {
        (False, False, False, False): " ",
        (True, True, False, False): "│",
        (False, False, True, True): "─",
        (True, True, True, True): "┼",
        (True, False, False, True): "└",
        (True, False, True, False): "┘",
        (False, True, False, True): "┌",
        (False, True, True, False): "┐",
        (True, True, False, True): "├",
        (True, True, True, False): "┤",
        (False, True, True, True): "┬",
        (True, False, True, True): "┴",
        (True, False, False, False): "╵",
        (False, True, False, False): "╷",
        (False, False, True, False): "╴",
        (False, False, False, True): "╶",
    }

color_mngmnt = [
        "=== Color Management ===",
        "1. Maze Color",
        "2. Path Color",
        "3. 42 Color",
        "4. Entry/Exit Color",
        "5. Quit"
    ]

choice = [
    "1. Green",
    "2. Blue",
    "3. Red",
    "4. Yellow",
    "5. Magenta",
    "6. Cyan",
    "7. White",
]
