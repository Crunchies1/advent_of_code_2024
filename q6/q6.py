from helpers.helpers import parse_input_file_2d_array

def main():
    guard_map: list[list[int]] = parse_input_file_2d_array('q6/input.txt')
    current_location: tuple[int, int] = initial_guard_location(guard_map)
    total_loops: int = 0
    for i, row in enumerate(guard_map):
        for j, col in enumerate(row):
            if col == ".":
                # Backtrack to original state after modification
                guard_map[i][j] = "#"
                if walk_until_loop_or_out(guard_map, current_location):
                    total_loops += 1
                guard_map[i][j] = "."
    print(total_loops)

def initial_guard_location(guard_map: list[list[int]]) -> tuple[int, int]:
    for i, row in enumerate(guard_map):
        for j, col in enumerate(row):
            if col == "^":
                return (i, j)
    return (0, 0)


# True if loop, False if out
def walk_until_loop_or_out(guard_map: list[list[int]], initial_guard_location: tuple[int, int]) -> bool:
    visited: set[tuple[tuple[int, int], str]] = set()
    current_location = initial_guard_location
    direction = "UP"
    while direction != "OUT":
        if (current_location, direction) not in visited:
            visited.add((current_location, direction))
        else:
            return True

        current_location, direction = next_location_direction(guard_map, current_location, direction)
    return False


def next_location_direction(guard_map: list[list[int]], current_location: tuple[int, int], direction: str) -> tuple[tuple[int, int], str]:
    match direction:
        case "LEFT":
            next_location = (current_location[0], current_location[1] - 1)
            if guard_is_out(guard_map, next_location):
                return (next_location, "OUT")
            if guard_hits_obstacle(guard_map, next_location):
                return next_location_direction(guard_map, current_location, "UP")
            return (next_location, "LEFT")
        case "UP":
            next_location = (current_location[0] - 1, current_location[1])
            if guard_is_out(guard_map, next_location):
                return (next_location, "OUT")
            if guard_hits_obstacle(guard_map, next_location):
                return next_location_direction(guard_map, current_location, "RIGHT")
            return (next_location, "UP")
        case "RIGHT":
            next_location = (current_location[0], current_location[1] + 1)
            if guard_is_out(guard_map, next_location):
                return (next_location, "OUT")
            if guard_hits_obstacle(guard_map, next_location):
                return next_location_direction(guard_map, current_location, "DOWN")
            return (next_location, "RIGHT")
        case "DOWN":
            next_location = (current_location[0] + 1, current_location[1])
            if guard_is_out(guard_map, next_location):
                return (next_location, "OUT")
            if guard_hits_obstacle(guard_map, next_location):
                return next_location_direction(guard_map, current_location, "LEFT")
            return (next_location, "DOWN")

def guard_hits_obstacle(guard_map: list[list[int]], location: tuple[int, int]) -> bool:
    return guard_map[location[0]][location[1]] == "#"

def guard_is_out(guard_map: list[list[int]], location: tuple[int, int]) -> bool:
    return (location[0] < 0 or location[0] >= len(guard_map)) or (location[1] < 0 or location[1] >= len(guard_map[0]))

main()