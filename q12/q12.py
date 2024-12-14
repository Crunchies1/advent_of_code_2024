from helpers.helpers import parse_input_file_2d_array
from collections import deque

def main():
    plant_map: list[list[str]] = parse_input_file_2d_array("q12/input.txt")
    print(find_region_price(plant_map))

def find_region_price(plant_map: list[list[str]]) -> int:
    visited: set[tuple[int, int]] = set()
    total_price: int = 0

    def bfs(start_coordinate: tuple[int, int]) -> int:
        plant_type: str = plant_map[start_coordinate[0]][start_coordinate[1]]
        directions: list[tuple[int, int]] = [[0, -1], [0, 1], [-1, 0], [1, 0]]
        queue: deque[tuple[int, int]] = deque([start_coordinate])
        region_coordinates: list[tuple[int, int]] = []
        total_area: int = 0
        total_perimeter: int = 0

        while queue:
            cur_coordinate = queue.popleft()
            cur_row, cur_col = cur_coordinate

            total_area += 1
            region_coordinates.append(cur_coordinate)
            visited.add(cur_coordinate)

            for direction in directions:
                dir_row, dir_col = direction
                new_row: int = cur_row + dir_row
                new_col: int = cur_col + dir_col

                if 0 <= new_row < len(plant_map) and 0 <= new_col < len(plant_map[0]):
                    if plant_map[new_row][new_col] != plant_type:
                        total_perimeter += 1

                    if (new_row, new_col) not in visited \
                        and plant_map[new_row][new_col] == plant_type \
                        and (new_row, new_col) not in queue:
                        queue.append((new_row, new_col))

                else:
                    total_perimeter += 1

        total_sides = get_num_sides(region_coordinates)
        print(plant_type, total_area, total_sides)

        return total_area * total_sides

    for row in range(len(plant_map)):
        for col in range(len(plant_map[0])):
            if (row, col) not in visited:
                total_price += bfs((row, col))

    return total_price

# We need something that can traverse the region, counting the number of sides
# In my head, to count the number of sides, can traverse the plants clockwise 
# until we reach the starting point
def get_num_sides(region_coordinates: list[tuple[int, int]]) -> int:
    num_sides: int = 1
    # Going to define up as 0, right as 1, down as 2, left as 3
    region_coordinate_sides: list[tuple[int, int, int]] = []
    for region_coordinate in region_coordinates:
        row, col = region_coordinate
        region_coordinate_sides.append((row, col, 0))
        region_coordinate_sides.append((row, col, 1))
        region_coordinate_sides.append((row, col, 2))
        region_coordinate_sides.append((row, col, 3))

    remove_matching_sides(region_coordinate_sides)
    # print(region_coordinate_sides, len(region_coordinate_sides))
    # Exhausting all the sides of the region, going clockwise
    current_coordinate = region_coordinate_sides.pop(0)
    total_rotations = 0
    while region_coordinate_sides:
        row, col, side = current_coordinate
        # Rotating around a single coordinate
        if total_rotations == 3:
            current_coordinate = region_coordinate_sides.pop(0)
            continue

        if side == 0: # Top side
            current_coordinate, extra_sides, same_block = process_side(region_coordinate_sides, current_coordinate, row, col + 1, 1)
            # print(current_coordinate, "top", len(region_coordinate_sides), extra_sides)
        elif side == 1: # Right side
            current_coordinate, extra_sides, same_block = process_side(region_coordinate_sides, current_coordinate, row + 1, col, 2)
            # print(current_coordinate, "right", len(region_coordinate_sides), extra_sides)
        elif side == 2: # Bottom side
            current_coordinate, extra_sides, same_block = process_side(region_coordinate_sides, current_coordinate, row, col - 1, 3)
            # print(current_coordinate, "bottom", len(region_coordinate_sides), extra_sides)
        else: # Left side
            current_coordinate, extra_sides, same_block = process_side(region_coordinate_sides, current_coordinate, row - 1, col, 0)
            # print(current_coordinate, "left", len(region_coordinate_sides), extra_sides)
        
        num_sides += extra_sides
        if same_block:
            total_rotations += 1
        else:
            total_rotations = 0
                        
    return num_sides

# The row and column refers to the next coordinate to check
# We also need to check if the next coordinate's side is 
# not blocked by another matching coordinate
# If it is, we need to increment the number of sides
def process_side(
        region_coordinate_sides: list[tuple[int, int, int]], 
        current_coordinate: tuple[int, int], 
        row: int, 
        col: int, 
        next_side: int
        ) -> tuple[tuple[int, int, int], int]:
    num_sides: int = 0
    same_block: bool = False
    # If we can continue in the same direction along a side, we do so
    cur_row, cur_col, cur_side = current_coordinate
    if (row, col, cur_side) in region_coordinate_sides:
        # print("continue")
        current_coordinate = (row, col, cur_side)
        region_coordinate_sides.remove((row, col, cur_side))
    # If instead we have to change direction (cliff), we increment the number of sides
    elif (cur_row, cur_col, next_side) in region_coordinate_sides:
        # print("cliff")
        num_sides += 1
        current_coordinate = (cur_row, cur_col, next_side)
        region_coordinate_sides.remove((cur_row, cur_col, next_side))
        same_block = True
    # If we are blocked by a wall, we increment the number of sides and go anti-clockwise
    elif anti_clockwise(cur_row, cur_col, cur_side) in region_coordinate_sides:
        # print("wall")
        num_sides += 1
        current_coordinate = anti_clockwise(cur_row, cur_col, cur_side)
        region_coordinate_sides.remove(anti_clockwise(cur_row, cur_col, cur_side))
    # In this case, we have finished traversing the wall
    # So move on to any leftover coordinates, otherwise we are done
    else: 
        # print("done")
        if not region_coordinate_sides:
            return None, num_sides, same_block
        else: 
            current_coordinate = region_coordinate_sides.pop(0)
            row, col, side = current_coordinate
            if not has_adjacent_coordinate(region_coordinate_sides, row, col, side):
                num_sides += 1
                

    return current_coordinate, num_sides, same_block

def anti_clockwise(row: int, col: int, side: int) -> tuple[int, int, int]:
    if side == 0:
        return row - 1, col + 1, 3
    elif side == 1:
        return row + 1, col + 1, 0
    elif side == 2:
        return row + 1, col - 1, 1
    else:
        return row - 1, col - 1, 2
 
# Preprocess and remove all sides which are touching each other already 
def remove_matching_sides(region_coordinate_sides: list[tuple[int, int, int]]) -> None:
    to_remove = []
    for row, col, side in region_coordinate_sides:
        opp_row, opp_col, opp_side = find_matching_side(row, col, side)
        if (opp_row, opp_col, opp_side) in region_coordinate_sides:
            to_remove.append((row, col, side))
    for side in to_remove:
        region_coordinate_sides.remove(side)

def find_matching_side(row: int, col: int, side: int) -> tuple[int, int, int]:
    if side == 0:
        return row - 1, col, 2
    elif side == 1:
        return row, col + 1, 3
    elif side == 2:
        return row + 1, col, 0
    else:
        return row, col - 1, 1

def has_adjacent_coordinate(region_coordinate_sides: list[tuple[int, int, int]], row: int, col: int, side: int) -> bool:
    if side == 0:
        return (row, col - 1, 0) in region_coordinate_sides or (row, col + 1, 0) in region_coordinate_sides
    elif side == 1:
        return (row - 1, col, 1) in region_coordinate_sides or (row + 1, col, 1) in region_coordinate_sides
    elif side == 2:
        return (row, col - 1, 2) in region_coordinate_sides or (row, col + 1, 2) in region_coordinate_sides
    else:
        return (row - 1, col, 3) in region_coordinate_sides or (row + 1, col, 3) in region_coordinate_sides


main()




