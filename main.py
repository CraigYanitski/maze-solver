from graphics import Window
from maze import Cell, Maze
from colorama import init, Fore

init(autoreset=True)


def main():
    num_rows, num_cols = 24, 32
    margin = 50
    screen_x, screen_y = 1600, 900
    cell_x, cell_y = (screen_x - 2*margin) / num_cols, (screen_y - 2*margin) / num_rows
    win = Window(screen_x, screen_y)
    maze = Maze(margin, margin, num_rows, num_cols, cell_x, cell_y, win, width=4)
    if maze.solve():
        print(Fore.GREEN + "Maze solved!!")
    else:
        print(Fore.RED + "Maze not solved...")
    win.wait_for_close()
    return


if __name__ == "__main__":
    main()
