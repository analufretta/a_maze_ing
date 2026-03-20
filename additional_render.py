import curses
from constant_args import CELL_HEIGHT, CELL_WIDTH, color_mngmnt, choice, State


def color_initializer(stdscr: "curses.window") -> list[int]:
    """Initialize curses color pairs and return a list of color attributes.

    Args:
        stdscr: A curses window object.

    Returns:
        A list of curses color pair attributes (1-7).
    """
    curses.start_color()

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)

    colors = [
        curses.color_pair(1),
        curses.color_pair(2),
        curses.color_pair(3),
        curses.color_pair(4),
        curses.color_pair(5),
        curses.color_pair(6),
        curses.color_pair(7),
    ]

    return colors


def color_management(stdscr: "curses.window", state: State) -> None:
    """Provide interactive menu for managing maze element colors.

    Displays options to change maze, player, 42 cell, and exit colors.
    Users select and customize each color from a palette using keyboard input.

    Args:
        stdscr: A curses window object.
        state: The State object containing color and display configuration.
    """
    y, x = stdscr.getmaxyx()
    middle_y = y // 2
    middle_x = x // 2
    stdscr.clear()

    def display_commands() -> None:
        """Display the color management menu options"""
        stdscr.clear()
        for i, item in enumerate(color_mngmnt):
            stdscr.addstr(middle_y + i, middle_x, item)
        stdscr.refresh()

    def display_colors(to_change: str) -> None:
        """Display available colors and allow user to select one.

        Args:
            to_change: state attribute name to update with the selected color.
        """
        while True:
            stdscr.clear()
            stdscr.addstr(middle_y - 1, middle_x, "=== Choose color ===")
            for i, item in enumerate(choice):
                stdscr.addstr(middle_y + i, middle_x, item)
                stdscr.addstr(
                    middle_y + i,
                    middle_x + 10,
                    " ▆",
                    state.COLORS[i],
                )
            stdscr.addstr(middle_y + i + 1, middle_x, "8. Return")
            stdscr.refresh()

            key = stdscr.getch()
            if key == ord("8"):
                break
            if ord("1") <= key <= ord("7"):
                setattr(state, to_change, key - ord("1"))
                break

    def choice_mngmt() -> None:
        """Handle user menu selection and manage color change flow."""
        while True:
            display_commands()
            key = stdscr.getch()

            if key == ord("1"):
                to_change = "m_color"
            elif key == ord("2"):
                to_change = "p_color"
            elif key == ord("3"):
                to_change = "color_42"
            elif key == ord("4"):
                to_change = "e_color"
            elif key == ord("5"):
                return
            else:
                continue

            display_colors(to_change)

    choice_mngmt()


def solve_it_yourself(stdscr: "curses.window", state: State) -> None:
    """Allow user to manually navigate and solve the maze using arrow keys.

    Displays the maze with the player character and handles movement input.
    The game concludes when the player reaches the exit point.

    Args:
        stdscr: A curses window object.
        state: The State object containing maze data and player position.
    """
    from render import get_maze_offsets

    color = state.COLORS[state.p_color]
    offset_y, offset_x, _, _ = get_maze_offsets(stdscr, state)
    e_point = state.exit_
    maze = state.maze
    p1 = state.player

    while True:
        row = p1[0]
        col = p1[1]
        current_cell = maze[row][col]

        if row == e_point[0] and col == e_point[1]:
            stdscr.clear()
            stdscr.addstr(20, 20, "Congrats, you've solved the maze")
            stdscr.refresh()
            stdscr.getch()
            break

        try:
            key = stdscr.getkey()
        except Exception:
            key = None

        def fail_move() -> None:
            """Display a failure message when the player hits a maze wall."""
            stdscr.clear()
            stdscr.addstr(20, 20, "be more careful looser")
            stdscr.refresh()
            stdscr.getch()

        if key == "KEY_LEFT":
            if not bool(current_cell & 0b1000):
                p1 = (row, col - 1)
            else:
                fail_move()
                break
        elif key == "KEY_RIGHT":
            if not bool(current_cell & 0b0010):
                p1 = (row, col + 1)
            else:
                fail_move()
                break
        elif key == "KEY_UP":
            if not bool(current_cell & 0b0001):
                p1 = (row - 1, col)
            else:
                fail_move()
                break
        elif key == "KEY_DOWN":
            if not bool(current_cell & 0b0100):
                p1 = (row + 1, col)
            else:
                fail_move()
                break
        else:
            p1 = p1

        stdscr.addstr(
            p1[0] * CELL_HEIGHT + 1 + offset_y,
            p1[1] * CELL_WIDTH + 1 + offset_x,
            "█",
            color,
        )
        stdscr.refresh()
