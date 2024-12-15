from helpers.helpers import parse_input_file_2d_array, parse_input_file_single_string

MOVEMENT_MAP = {
    "^": [-1, 0],
    "v": [1, 0],
    "<": [0, -1],
    ">": [0, 1]
}
ROBOT = "@"
ROCK = "O"
WALL = "#"
EMPTY = "."

def main():
    maze = parse_input_file_2d_array("q15/maze.txt")
    actions = parse_input_file_single_string("q15/input.txt")
    robot = []
    for row, row_val in enumerate(maze):
        for col, col_val in enumerate(row_val):
            if col_val == ROBOT:
                robot = [row, col]

    for row in maze:
        print("".join(row))
    for action in actions:
        print(action)
        move_robot(maze, robot, action)
        for row in maze:
            print("".join(row))

    print(calculate_rock_scores(maze))

def calculate_rock_scores(maze: list[list[str]]) -> int:
    total_score: int = 0
    for row, row_val in enumerate(maze):
        for col, col_val in enumerate(row_val):
            if col_val == ROCK:
                total_score += (row * 100 + col)
    return total_score

def move_robot(maze: list[list[str]], robot: list[int], action: str) -> None:
    row: int = robot[0]
    col: int = robot[1]
    if action in MOVEMENT_MAP:
        row_dir: int = MOVEMENT_MAP[action][0]
        col_dir: int = MOVEMENT_MAP[action][1]
        if maze[row + row_dir][col + col_dir] == EMPTY:
            maze[row][col] = EMPTY
            maze[row + row_dir][col + col_dir] = ROBOT
            robot[0] += row_dir
            robot[1] += col_dir
        elif maze[row + row_dir][col + col_dir] == ROCK:
            if push_rock(maze, row + row_dir, col + col_dir, action):
                maze[row][col] = EMPTY
                robot[0] += row_dir
                robot[1] += col_dir
        
# Assume the tile we push is a rock
def push_rock(maze: list[list[str]], row: int, col: int, direction: str) -> bool:
    row_dir: int = MOVEMENT_MAP[direction][0]
    col_dir: int = MOVEMENT_MAP[direction][1]
    empty_space, empty_row, empty_col = has_empty_space(maze, row, col, direction)
    if empty_space:
        maze[row][col] = ROBOT
        row += row_dir
        col += col_dir
        print("Moving rock to", row, col)
        while row != empty_row or col != empty_col:
            print("Moving rock to", row, col)
            maze[row][col] = ROCK
            row += row_dir
            col += col_dir
        maze[row][col] = ROCK
        return True
    return False
    

def has_empty_space(maze: list[list[str]], row: int, col: int, direction: int) -> tuple[bool, int, int]:
    row_dir: int = MOVEMENT_MAP[direction][0]
    col_dir: int = MOVEMENT_MAP[direction][1]
    while maze[row][col] == ROCK:
        row += row_dir
        col += col_dir
    if maze[row][col] == EMPTY:
        print("Empty space found at", row, col)
        return True, row, col
    return False, row, col

main()