from helpers.helpers import parse_input_file_2d_array, parse_input_file_single_string

MOVEMENT_MAP = {
    "^": [-1, 0],
    "v": [1, 0],
    "<": [0, -1],
    ">": [0, 1]
}
ROBOT = "@"
ROCK = "O"
LEFT_ROCK = "["
RIGHT_ROCK = "]"
WALL = "#"
EMPTY = "."

def main():
    maze = parse_input_file_2d_array("q15/maze.txt")
    maze = widen_maze(maze)
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

def widen_maze(maze: list[list[str]]) -> list[list[str]]:
    new_maze = []
    for row in maze:
        widened_row = []
        for col in row:
            if col == ROCK:
                widened_row.append("[")
                widened_row.append("]")
            elif col == WALL:
                widened_row.append(WALL)
                widened_row.append(WALL)
            elif col == ROBOT:
                widened_row.append(ROBOT)
                widened_row.append(EMPTY)
            else:
                widened_row.append(EMPTY)
                widened_row.append(EMPTY)
        new_maze.append(widened_row)
    return new_maze

def calculate_rock_scores(maze: list[list[str]]) -> int:
    total_score: int = 0
    for row, row_val in enumerate(maze):
        for col, col_val in enumerate(row_val):
            if col_val == LEFT_ROCK:
                total_score += (row * 100 + col)
    return total_score

def move_robot(maze: list[list[str]], robot: list[int], action: str) -> None:
    row: int = robot[0]
    col: int = robot[1]
    if action in MOVEMENT_MAP:
        row_dir: int = MOVEMENT_MAP[action][0]
        col_dir: int = MOVEMENT_MAP[action][1]
        # If the robot is moving to an empty space
        if maze[row + row_dir][col + col_dir] == EMPTY:
            maze[row][col] = EMPTY
            maze[row + row_dir][col + col_dir] = ROBOT
            robot[0] += row_dir
            robot[1] += col_dir
        # If the robot is moving into a rock
        elif maze[row + row_dir][col + col_dir] in [LEFT_ROCK, RIGHT_ROCK]:
            rock = get_rock(maze, row + row_dir, col + col_dir)
            print("Pushing rock: ", rock)
            if push_rock(maze, (row + row_dir, col + col_dir), rock, action):
                maze[row][col] = EMPTY
                robot[0] += row_dir
                robot[1] += col_dir
        
def get_rock(maze: list[list[str]], row: int, col: int) -> tuple[int, int, int, int]:
    if maze[row][col] == LEFT_ROCK:
        return (row, col, row, col + 1)
    if maze[row][col] == RIGHT_ROCK:
        return (row, col - 1, row, col)

# Assume the tile we push is a rock
def push_rock(maze: list[list[str]], new_robot: tuple[int, int], rock: tuple[int, int, int, int], direction: str) -> bool:
    row_dir: int = MOVEMENT_MAP[direction][0]
    col_dir: int = MOVEMENT_MAP[direction][1]
    empty_space, all_moved_rocks = has_empty_space(maze, rock, direction)
    print("Rocks to move", all_moved_rocks)
    if empty_space:
        # Set the new robot position
        maze[new_robot[0]][new_robot[1]] = ROBOT
        # Set the new rock positions
        for rock in all_moved_rocks:
            new_rock = (rock[0] + row_dir, rock[1] + col_dir, rock[2] + row_dir, rock[3] + col_dir)
            maze[new_rock[0]][new_rock[1]] = LEFT_ROCK
            maze[new_rock[2]][new_rock[3]] = RIGHT_ROCK
        # Clean up all hanging rocks
        for row, row_val in enumerate(maze):
            for col, col_val in enumerate(row_val):
                if col_val == LEFT_ROCK and row_val[col + 1] != RIGHT_ROCK:
                    maze[row][col] = EMPTY
                if col_val == RIGHT_ROCK and row_val[col - 1] != LEFT_ROCK:
                    maze[row][col] = EMPTY
        return True
    return False
    
# Now all the rocks which are pushed need to be moved to the empty space
def has_empty_space(maze: list[list[str]], rock: tuple[int, int, int, int], direction: int) -> tuple[bool, list[tuple[int, int, int, int]]]:
    all_rocks_moved: list[tuple[int, int, int, int]] = [rock]
    if direction in ["^", "v"]:
        # Check if there is empty space up or down ahead, while tracking all rocks
        new_rocks = rocks_up_down_ahead(maze, [rock], direction)
        if new_rocks == -1:
            return False, []
        all_rocks_moved.extend(new_rocks)
        while new_rocks:
            new_rocks = rocks_up_down_ahead(maze, new_rocks, direction)
            if new_rocks == -1:
                return False, []
            all_rocks_moved.extend(new_rocks)
        # There is empty space ahead
        return True, all_rocks_moved
    
    if direction in ["<", ">"]:
        # Check if there is empty space to the left or right
        new_rocks = rocks_left_right_ahead(maze, [rock], direction)
        if new_rocks == -1:
            return False, []
        all_rocks_moved.extend(new_rocks)
        while new_rocks:
            new_rocks = rocks_left_right_ahead(maze, new_rocks, direction)
            if new_rocks == -1:
                return False, []
            all_rocks_moved.extend(new_rocks)
        # There is empty space ahead
        return True, all_rocks_moved

def rocks_up_down_ahead(maze: list[list[str]], rocks: list[tuple[int, int, int, int]], direction: str) -> list[tuple[int, int, int, int]]:
    row_dir: int = MOVEMENT_MAP[direction][0]
    col_dir: int = MOVEMENT_MAP[direction][1]
    new_rocks: list[tuple[int, int, int, int]] = []
    for rock in rocks:
        left_row = rock[0] + row_dir
        left_col = rock[1] + col_dir
        right_row = rock[2] + row_dir
        right_col = rock[3] + col_dir
        if maze[left_row][left_col] == LEFT_ROCK: # Rock directly in front
            new_rocks.append((left_row, left_col, right_row, right_col))
        if maze[left_row][left_col] == RIGHT_ROCK: # Rock to the left side
            new_rocks.append((left_row, left_col - 1, left_row, left_col))
        if maze[right_row][right_col] == LEFT_ROCK: # Rock to the right side
            new_rocks.append((right_row, right_col, right_row, right_col + 1))
        if WALL in [maze[left_row][left_col], maze[right_row][right_col]]:
            return -1
    
    return new_rocks

def rocks_left_right_ahead(maze: list[list[str]], rocks: list[tuple[int, int, int, int]], direction: str) -> list[tuple[int, int, int, int]]:
    row_dir: int = MOVEMENT_MAP[direction][0]
    col_dir: int = MOVEMENT_MAP[direction][1]
    new_rocks: list[tuple[int, int, int, int]] = []
    for rock in rocks:
        # Set the new position we are looking at
        left_row = rock[0] + row_dir
        left_col = rock[1] + col_dir
        right_row = rock[2] + row_dir
        right_col = rock[3] + col_dir
        if maze[left_row][left_col] == RIGHT_ROCK and direction == "<": # Rock to the left side
            new_rocks.append((left_row, left_col - 1, left_row, left_col))
        if maze[right_row][right_col] == LEFT_ROCK and direction == ">": # Rock to the right side
            new_rocks.append((right_row, right_col, right_row, right_col + 1))
        if WALL in [maze[left_row][left_col], maze[right_row][right_col]]: # Wall either to right or left
            return -1
    
    return new_rocks

main()
