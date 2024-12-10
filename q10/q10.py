from helpers.helpers import parse_input_file_2d_array
from collections import deque

def main():
    trailhead_map = parse_input_file_2d_array("q10/input.txt")
    trailhead_map = [[int(char) for char in row] for row in trailhead_map]
    print(sum_trailheads(trailhead_map))

def sum_trailheads(trailhead_map: list[list[int]]) -> int:
    total_score: int = 0

    def bfs(current_position: tuple[int, int]) -> int:
        bfs_score: int = 0
        visited: set[tuple[int, int]] = set()
        # summed: set[tuple[int, int]] = set()
        directions: list[tuple[int, int]] = [
            (0, 1), (1, 0), (0, -1), (-1, 0)
        ]
        queue: deque[tuple[int, int]] = deque([current_position])
        while queue:
            row, col = queue.popleft()
            visited.add((row, col))

            if trailhead_map[row][col] == 9:
                # if (row, col) not in summed:
                    # summed.add((row, col))
                bfs_score += 1
                continue

            for row_dir, col_dir in directions:
                new_row, new_col = row + row_dir, col + col_dir
                if 0 <= new_row < len(trailhead_map) and 0 <= new_col < len(trailhead_map[0]):
                    if (new_row, new_col) not in visited and trailhead_map[new_row][new_col] == trailhead_map[row][col] + 1:
                        queue.append((new_row, new_col))

        return bfs_score

    for row in range(len(trailhead_map)):
        for col in range(len(trailhead_map[0])):
            if trailhead_map[row][col] == 0:
                total_score += bfs((row, col))

    return total_score

main()  
