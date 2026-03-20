
import sys
from file_config import FileConfig
from mazegen import MazeGenerator
from curses import wrapper
from render import display_main
from make_output_file import write_output_file


def main() -> None:
    """Run the maze application from command-line arguments.

    This function validates input arguments, loads the maze configuration,
    starts the interactive renderer, and writes the resulting maze to the
    configured output file. It exits with status code 1 when validation,
    rendering, or file writing fails.
    """
    if len(sys.argv) != 2:
        print("Argument not valid!\n"
              "Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    try:
        parse = FileConfig(sys.argv[1])
    except (FileNotFoundError, ValueError) as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    maze = MazeGenerator(parse.config)

    try:
        wrapper(lambda stdscr: display_main(stdscr, parse))
        render_error: ValueError | None = None
    except ValueError as e:
        print(f"Render error: {e}")
        render_error = e
    finally:
        try:
            write_output_file(maze.get_grid(), maze.get_entry(),
                              maze.get_exit(), maze.get_solution_dir(),
                              parse.output_file)
        except IOError as e:
            print(f"File Error: {e}")
            sys.exit(1)

    if render_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
