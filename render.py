import curses
import sys
from file_config import FileConfig
from mazegen.mazegen import MazeGenerator
from additional_render import (
    color_initializer,
    color_management,
    solve_it_yourself,
)
import time
from constant_args import (
    CELL_HEIGHT,
    CELL_WIDTH,
    corners,
    menu,
    State
)


def draw_path(stdscr: "curses.window", state: State) -> None:
    """Animate and display the solution path through the maze.

    Args:
        stdscr: A curses window object.
        state: The State object containing maze data and path information.
    """
    stdscr.refresh()
    OFFSET_Y, OFFSET_X, h_maze, w_maze = get_maze_offsets(stdscr, state)
    color = state.COLORS[state.p_color]
    entry_y, entry_x = state.entry
    exit_y, exit_x = state.exit_
    path = state.path
    stdscr.nodelay(True)
    for y, x in path:
        if (y, x) == (entry_y, entry_x) or (y, x) == (exit_y, exit_x):
            continue
        key = stdscr.getch()
        if key != -1:
            for row, cols in path:
                if (row, cols) != (entry_y, entry_x):
                    if (row, cols) != (exit_y, exit_x):
                        stdscr.addstr(
                            row * CELL_HEIGHT + 1 + OFFSET_Y,
                            cols * CELL_WIDTH + 1 + OFFSET_X,
                            "██",
                            color,
                        )
            break
        stdscr.addstr(
            y * CELL_HEIGHT + 1 + OFFSET_Y,
            x * CELL_WIDTH + 1 + OFFSET_X,
            "██",
            color,
        )
        stdscr.refresh()
        time.sleep(0.1)
    stdscr.nodelay(False)
    stdscr.refresh()


def get_maze_offsets(stdscr: "curses.window",
                     state: State) -> tuple[int, int, int, int]:
    """Calculate the offsets for centering the maze on the screen.

    Args:
        stdscr: A curses window object.
        state: The State object containing maze dimensions.

    Returns:
        A tuple of (offset_y, offset_x, maze_height, maze_width).
    """
    height, width = stdscr.getmaxyx()
    rows = state.rows
    cols = state.cols
    h_maze = rows * CELL_HEIGHT + 1
    w_maze = cols * CELL_WIDTH + 1
    OFFSET_Y = (height - h_maze) // 2
    OFFSET_X = (width - w_maze) // 2
    return OFFSET_Y, OFFSET_X, h_maze, w_maze


def display_commands(stdscr: "curses.window", state: State) -> None:
    """Display the interactive command menu at the bottom of the screen.

    Args:
        stdscr: A curses window object.
        state: The State object containing maze positioning information.
    """
    height, width = stdscr.getmaxyx()
    OFFSET_Y, OFFSET_X, h_maze, w_maze = get_maze_offsets(stdscr, state)
    start = OFFSET_Y + h_maze
    middle = OFFSET_X + w_maze // 2
    space = height - start
    if space <= 1:
        return
    if space > len(menu) + 1:
        for i, item in enumerate(menu):
            stdscr.addstr(start + i + 1, middle - 9, item)
    else:
        stdscr.addstr(
            height - 1, 0,
            "1.Regenerate | 2. Show/Hide Path | 3. Rotate colors"
            " | 4. Colors Manager | 5. Solve it | 6.Quit")
    stdscr.refresh()


def command_mngmnt(stdscr: "curses.window", state: State) -> None:
    """Handle user input and execute corresponding maze control commands.

    Supports regenerating maze, toggling path display, rotating colors,
    opening color manager, solving maze, and quitting the application.

    Args:
        stdscr: A curses window object.
        state: The State object containing maze and configuration data.
    """
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord("1"):
            infos = FileConfig(sys.argv[1])
            state = maze_initialization(stdscr, infos, state)
            display_maze(stdscr, state)
            stdscr.refresh()
        elif key == ord("2"):
            state.show_path = not state.show_path
            display_maze(stdscr, state)
            stdscr.refresh()
        elif key == ord("3"):
            state.m_color = (state.m_color + 1) % len(state.COLORS)
            state.p_color = (state.p_color + 1) % len(state.COLORS)
            state.color_42 = (state.color_42 + 1) % len(state.COLORS)
            state.e_color = (state.e_color + 1) % len(state.COLORS)
            display_maze(stdscr, state)
            stdscr.refresh()
        elif key == ord("4"):
            color_management(stdscr, state)
            display_maze(stdscr, state)
            stdscr.refresh()
        elif key == ord("5"):
            state.show_path = False
            solve_it_yourself(stdscr, state)
            display_maze(stdscr, state)
        elif key == ord("6"):
            return
        stdscr.refresh()


def display_maze(stdscr: "curses.window", state: State) -> None:
    """Render the complete maze with walls, paths, entry/exit points, and menu.

    Args:
        stdscr: A curses window object.
        state: The State object containing maze data and display configuration.

    Raises:
        ValueError: If the terminal is too small to display the maze.
    """
    stdscr.clear()
    wall_color = state.COLORS[state.m_color]
    maze = state.maze
    rows = state.rows
    cols = state.cols
    OFFSET_Y, OFFSET_X, h_maze, w_maze = get_maze_offsets(stdscr, state)
    height, width = stdscr.getmaxyx()
    if height < rows * CELL_HEIGHT + 1:
        raise ValueError("The height provided is too high. Chill down.")
    if width < cols * CELL_WIDTH + 1:
        raise ValueError("The width provided is too large. Chill down.")
    for cy in range(rows + 1):
        for cx in range(cols + 1):
            if cy == 0 and cx == 0:
                up = False
                down = True
                left = False
                right = True
            elif cy == 0 and cx == cols:
                up = False
                down = True
                left = True
                right = False
            elif cy == 0:
                up = False
                down = (
                    bool(maze[cy][cx - 1] & 0b0010)
                    if cy < rows and cx > 0
                    else False
                )
                left = cx > 0
                right = cx < cols
            elif cx == 0 and cy == rows:
                up = True
                down = False
                left = False
                right = True
            elif cx == 0:
                up = cy > 0
                down = cy < rows
                left = False
                right = (
                    bool(maze[cy - 1][cx] & 0b0100)
                    if cy > 0 and cx < cols
                    else False
                )
            else:
                up = (
                    bool(maze[cy - 1][cx - 1] & 0b0010)
                    if cy > 0 and cx > 0
                    else False
                )
                down = (
                    bool(maze[cy][cx - 1] & 0b0010)
                    if cy < rows and cx > 0
                    else False
                )
                left = (
                    bool(maze[cy - 1][cx - 1] & 0b0100)
                    if cy > 0 and cx > 0
                    else False
                )
                right = (
                    bool(maze[cy - 1][cx] & 0b0100)
                    if cy > 0 and cx < cols
                    else False
                )
            char = corners.get((up, down, left, right), "?")
            stdscr.addstr(
                cy * CELL_HEIGHT + OFFSET_Y,
                cx * CELL_WIDTH + OFFSET_X,
                char,
                wall_color,
            )
            if cx < cols:
                h_char = "───" if right else "   "
                stdscr.addstr(
                    cy * CELL_HEIGHT + OFFSET_Y,
                    cx * CELL_WIDTH + 1 + OFFSET_X,
                    h_char,
                    wall_color,
                )
        if cy < rows and cx > 0:
            for cx in range(cols + 1):
                if cx == 0:
                    v_char = "│"
                    stdscr.addstr(
                        cy * CELL_HEIGHT + 1 + OFFSET_Y,
                        cx * CELL_WIDTH + OFFSET_X,
                        v_char,
                        wall_color,
                    )
                else:
                    has_wall = cx > 0 and bool(maze[cy][cx - 1] & 0b0010)
                    v_char = "│" if has_wall else " "
                    stdscr.addstr(
                        cy * CELL_HEIGHT + 1 + OFFSET_Y,
                        cx * CELL_WIDTH + OFFSET_X,
                        v_char,
                        wall_color,
                    )
                if cx < cols:
                    stdscr.addstr(
                        cy * CELL_HEIGHT + 1 + OFFSET_Y,
                        cx * CELL_WIDTH + 1 + OFFSET_X,
                        " ",
                    )
    color_42 = state.COLORS[state.color_42]
    for row in range(rows):
        for col in range(cols):
            if maze[row][col] == 0xF:
                screen_y = row * CELL_HEIGHT + 1 + OFFSET_Y
                screen_x = col * CELL_WIDTH + 1 + OFFSET_X
                stdscr.addstr(screen_y, screen_x, "███", color_42)
    p_entry = state.entry
    p_exit = state.exit_
    point_color = state.COLORS[state.e_color]
    stdscr.addstr(
        p_entry[1] * CELL_HEIGHT + 1 + OFFSET_Y,
        p_entry[0] * CELL_WIDTH + 1 + OFFSET_X,
        "E",
        point_color,
    )
    stdscr.addstr(
        p_exit[1] * CELL_HEIGHT + 1 + OFFSET_Y,
        p_exit[0] * CELL_WIDTH + 1 + OFFSET_X,
        "X",
        point_color,
    )
    display_commands(stdscr, state)
    if state.show_path:
        draw_path(stdscr, state)
    stdscr.refresh()


def maze_initialization(stdscr: "curses.window", infos: FileConfig,
                        existing_state: State | None = None) -> State:
    """Initialize maze state with generated maze and color configuration.

    Args:
        stdscr: A curses window object.
        infos: FileConfig containing maze configuration parameters.
        existing_state: Optional State to preserve color settings

    Returns:
        A State object initialized with maze data and configuration.
    """
    colors = color_initializer(stdscr)
    maze = MazeGenerator(infos.config)
    state = State(
        maze=maze.get_grid(),
        rows=infos.config.height,
        cols=infos.config.width,
        m_color=existing_state.m_color if existing_state else 0,
        color_42=existing_state.color_42 if existing_state else 1,
        p_color=existing_state.p_color if existing_state else 2,
        e_color=existing_state.e_color if existing_state else 3,
        show_path=False,
        path=maze.get_solution_coord(),
        entry=maze.get_entry(),
        exit_=maze.get_exit(),
        COLORS=colors,
        player=maze.get_entry(),
    )
    return state


def display_main(stdscr: "curses.window", infos: FileConfig) -> None:
    """Main entry point for the maze rendering application.

    Initializes the maze, displays it, and starts the command management loop.

    Args:
        stdscr: A curses window object.
        infos: FileConfig containing maze configuration parameters.
    """
    curses.curs_set(0)

    state = maze_initialization(stdscr, infos)
    display_maze(stdscr, state)
    command_mngmnt(stdscr, state)
