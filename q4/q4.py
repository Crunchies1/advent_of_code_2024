from helpers.helpers import parse_input_file_2d_array

def main():
    grid: list[list[str]] = parse_input_file_2d_array("q4/input.txt")
    print(search_grid_for_xmas(grid))

# This function is called for every "X" in the grid
def search_grid_for_xmas(grid: list[list[str]]) -> int:
    xmas_count: int = 0
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "A":
                print(f"searching for xmas at {row}, {col}")
                xmas_count += search_for_cross_mas((row, col), grid)
    return xmas_count

# This function is called assuming the current coordinate is an "X"
def search_for_xmas(coordinate: tuple[int, int], grid: list[list[str]]) -> int:
    row, col = coordinate
    directions: list[tuple[int, int]] = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
    xmas_count: int = 0
    for direction in directions:
        new_row: int = row
        new_col: int = col
        xmas_condition: list[str] = ["M", "A", "S"]

        while xmas_condition:
            new_row += direction[0]
            new_col += direction[1]
            # The new coordinate is out of bounds
            if new_row < 0 or new_row >= len(grid) or new_col < 0 or new_col >= len(grid[0]):
                print("oob")
                break
            # The XMAS string is not found
            if grid[new_row][new_col] != xmas_condition[0]:
                print("not found")
                break
            xmas_condition.pop(0)
            print(xmas_condition)

        if not xmas_condition:
            xmas_count += 1

    return xmas_count

def search_for_cross_mas(coordinate: tuple[int, int], grid: list[list[str]]) -> int:
    # Exit early if coordinate is on the edge of the grid
    if coordinate[0] == 0 or coordinate[0] == len(grid) - 1 or coordinate[1] == 0 or coordinate[1] == len(grid[0]) - 1:
        return 0
    row, col = coordinate
    # orthogonal_crosses: list[tuple[int, int]] = [[(0, 1), (0, -1)], [(1, 0), (-1, 0)]]
    diagonal_crosses: list[tuple[int, int]] = [[(1, 1), (-1, -1)], [(-1, 1), (1, -1)]]

    # orthogonal_cross_count: int = 1
    # for direction in orthogonal_crosses:
    #     right = direction[0]
    #     left = direction[1]
    #     right_row = row + right[0]
    #     right_col = col + right[1]
    #     left_row = row + left[0]
    #     left_col = col + left[1]
    #     if not ((search_for_m((right_row, right_col), grid) and search_for_s((left_row, left_col), grid)) or (search_for_m((left_row, left_col), grid) and search_for_s((right_row, right_col), grid))):
    #         orthogonal_cross_count = 0
    #         break

    diagonal_cross_count: int = 1
    for direction in diagonal_crosses:
        right = direction[0]
        left = direction[1]
        right_row = row + right[0]
        right_col = col + right[1]
        left_row = row + left[0]
        left_col = col + left[1]
        if not ((search_for_m((right_row, right_col), grid) and search_for_s((left_row, left_col), grid)) or (search_for_m((left_row, left_col), grid) and search_for_s((right_row, right_col), grid))):
            diagonal_cross_count = 0
            break

    return diagonal_cross_count

def search_for_m(coordinate: tuple[int, int], grid: list[list[str]]) -> bool:
    if grid[coordinate[0]][coordinate[1]] == "M":
        return True
    return False

def search_for_s(coordinate: tuple[int, int], grid: list[list[str]]) -> bool:
    if grid[coordinate[0]][coordinate[1]] == "S":
        return True
    return False

main()